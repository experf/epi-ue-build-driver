from pathlib import PureWindowsPath
from typing import Dict

from nansi.plugins.action.compose import ComposeAction
from nansi.plugins.action.args.all import Arg, ArgsBase
from nansi.os_resolve import os_map_resolve

from ._common import cast_pure_windows_path


class Args(ArgsBase):
    service_name = Arg(str, "epi-ue-build-driver")
    service_port = Arg(int, 5000)
    python_version = Arg(str, "3.9.2")


class WindowsArgs(Args):
    python_home = Arg(
        PureWindowsPath,
        default=lambda self, arg: self.default_python_home,
        cast=cast_pure_windows_path,
    )

    pywin32_version = Arg(str, ">=301")

    @property
    def python_major_minor_str(self):
        """
        >>> WindowsArgs({"python_version": "3.9.2"}, {}).python_major_minor_str
        '39'
        """
        return "".join(self.python_version.split(".")[0:2])

    @property
    def default_python_home(self) -> PureWindowsPath:
        """
        >>> WindowsArgs(
        ...     {"python_version": "3.9.2"},
        ...     {}
        ... ).default_python_home
        PureWindowsPath('C:/Python39')
        """
        return PureWindowsPath(
            "C:\\",
            f"Python{self.python_major_minor_str}",
        )

    @property
    def python_site_packages(self) -> PureWindowsPath:
        return self.python_home / "Lib" / "site-packages"

    @property
    def python_exe(self) -> PureWindowsPath:
        return self.python_home / "python.exe"

    @property
    def pywintypes_dll_filename(self) -> str:
        return f"pywintypes{self.python_major_minor_str}.dll"

    @property
    def pywintypes_dll_src(self) -> PureWindowsPath:
        """
        Source location for the pywintypes `.dll` file that needs to be coppied
        from for the Python/Windows service stuff to work.

        ## See Also

        -   https://stackoverflow.com/a/51653500
        """
        return (
            self.python_site_packages
            / "pywin32_system32"
            / self.pywintypes_dll_filename
        )

    @property
    def pywintypes_dll_dest(self) -> PureWindowsPath:
        """
        Destination location for the pywintypes `.dll` file that needs to be
        coppied to for the Python/Windows service stuff to work.

        ## See Also

        -   https://stackoverflow.com/a/51653500
        """
        return (
            self.python_site_packages / "win32" / self.pywintypes_dll_filename
        )


class ActionModule(ComposeAction):
    def compose(self):
        os_map_resolve(
            self._task_vars["ansible_facts"],
            {
                "family": {
                    "windows": self.compose_windows,
                }
            },
        )()

    def pip_install_windows(
        self, task_args: WindowsArgs, cmd_args: str
    ) -> Dict:
        return self.tasks.ansible.windows.win_shell(
            f"{task_args.python_exe} -m pip install {cmd_args}"
        )

    def compose_windows(self):
        args = WindowsArgs(self._task.args, parent=self)

        # Disable UAC -- I don't recall why, but this was done to get some
        # install step to run
        disable_uac_result = self.tasks.ansible.windows.win_regedit(
            path="HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\policies\system",
            name="EnableLUA",
            data=0,
            type="dword",
            state="present",
        )

        # If we _did_ just disable UAC we need to reboot to see the effects
        if disable_uac_result.get("changed") is True:
            self.tasks.ansible.windows.win_reboot()

        self.tasks.chocolatey.chocolatey.win_chocolatey(
            name="python",
            state="present",
            version=args.python_version,
        )

        # I guess 'cause this uses `cmd.exe` (as opposed to PowerShell) you have
        # to use the executable path directly
        self.pip_install_windows(args, "--upgrade pip")
        self.pip_install_windows(args, f"pywin32{args.pywin32_version}")

        # SEE   https://stackoverflow.com/a/51653500
        self.tasks.ansible.windows.win_copy(
            src=args.pywintypes_dll_src,
            dest=args.pywintypes_dll_dest,
            remote_src=True,
        )

        self.tasks.community.windows.win_firewall_rule(
            name=args.service_name,
            localport=args.service_port,
            action="allow",
            direction="in",
            protocol="tcp",
            state="present",
            enabled="yes",
        )
