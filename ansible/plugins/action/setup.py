from nansi.plugins.action.compose import ComposeAction
from nansi.plugins.action.args import Arg, ArgsBase

class Args(ArgsBase):
    python_version = Arg(str)

class ActionModule(ComposeAction):
    def compose(self):
        args = Args(self._task.args, self._task_vars)

        disable_uac_result = self.tasks.win_regedit(
            path="HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\policies\system",
            name="EnableLUA",
            data=0,
            type="dword",
            state="present",
        )

        if disable_uac_result.get("changed") is True:
            self.tasks.win_reboot()

        self.tasks.win_chocolatey(
            name="python",
            state="present",

        )
