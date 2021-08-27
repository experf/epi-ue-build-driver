from pathlib import PureWindowsPath, Path
from typing import Dict
import subprocess
import sys

from nansi.plugins.action.compose import ComposeAction
from nansi.plugins.action.args.all import Arg, ArgsBase
from nansi.os_resolve import os_map_resolve

from ._common import cast_pure_windows_path


class Args(ArgsBase):
    src = Arg(Path)
    name = Arg(str, "epi-ue-build-driver")
    version = Arg(str, "0.1.0")
    wheel_filename = Arg(str, lambda self, arg: self.default_wheel_filename)
    wheel_src = Arg(Path, lambda self, arg: self.default_wheel_src)

    @property
    def default_wheel_filename(self) -> str:
        return f"{self.name.replace('-', '_')}-{self.version}-py3-none-any.whl"

    @property
    def default_wheel_src(self) -> Path:
        return self.src / "dist" / self.wheel_filename


class WindowsArgs(Args):
    python_version = Arg(str, "3.9.2")

    python_home = Arg(
        PureWindowsPath,
        default=lambda self, arg: self.default_python_home,
        cast=cast_pure_windows_path,
    )

    wheel_dest = Arg(
        PureWindowsPath,
        default=lambda self, _: self.default_wheel_dest,
        cast=cast_pure_windows_path,
    )

    service_human_name = Arg(str, "EPI UE Build Driver")

    @property
    def default_wheel_dest(self) -> PureWindowsPath:
        return PureWindowsPath("C:\\", "temp", self.wheel_filename)

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
    def python_exe(self) -> PureWindowsPath:
        return self.python_home / "python.exe"


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

    def build_wheel(self, args):
        # Build the package (locally)
        result = subprocess.run(
            [sys.executable, "setup.py", "bdist_wheel"],
            # shell=True,
            # check=True,
            cwd=args.src,
            encoding="utf-8",
            capture_output=True,
        )

        if result.returncode != 0:
            self.log.error(
                "Fuck",
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )
            result.check_returncode()

    def pip_install_windows(
        self, task_args: WindowsArgs, cmd_args: str
    ) -> Dict:
        return self.tasks.ansible.windows.win_shell(
            f"{task_args.python_exe} -m pip install {cmd_args}"
        )

    def compose_windows(self):
        args = WindowsArgs(self._task.args, parent=self)

        self.build_wheel(args)

        # Ensure the wheel destination's parent directory exists
        self.tasks.ansible.windows.win_file(
            path=str(args.wheel_dest.parent),
            state="directory",
        )

        # Copy the wheel
        self.tasks.ansible.windows.win_copy(
            src=str(args.wheel_src),
            dest=str(args.wheel_dest),
        )

        # Install the wheel!
        self.pip_install_windows(args, args.wheel_dest)

        # Install the service
        self.tasks.ansible.windows.win_shell(f"{args.name} install")

        # Start the service!
        self.tasks.ansible.windows.win_service(
            name=args.service_human_name,
            start_mode="auto",
            state="started",
        )
