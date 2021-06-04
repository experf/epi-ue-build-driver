# pylint: disable=wrong-import-position,line-too-long

# References
# ============================================================================
#
# 1.    https://devtut.github.io/python/creating-a-windows-service-using-python.html#running-a-flask-web-application-as-a-service
# 2.    https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
#

# import sys
# if sys.platform != "win32":
#     raise ImportError(
#         f"{__name__} is windows-only (sys.platform={sys.platform}"
#     )

import threading
import asyncio
import sys
from pathlib import Path

import win32serviceutil  # pylint: disable=import-error
import servicemanager  # pylint: disable=import-error
import win32service  # pylint: disable=import-error

from epi.ue.build.driver.server import Server
from epi.ue.build.driver.helpers import get_or_create_eventloop


class Service(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    # LOG_FORMATTER = logging.Formatter(
    #     "%(threadName)s %(levelname)s %(name)s %(message)s"
    # )
    # LOG_HANDLER = logging.FileHandler(
    #     Path("C:\\", "temp", "epi-ue-build-driver.log")
    # )
    # LOG_HANDLER.setFormatter(LOG_FORMATTER)

    _svc_name_ = "EPIUEBuildDriver"
    _svc_display_name_ = "EPI UE Build Driver"
    _svc_description_ = "Unreal Engine build driver"

    server: Server

    @staticmethod
    def log(message):
        servicemanager.LogInfoMsg(message)

    @staticmethod
    def log(message):
        servicemanager.LogInfoMsg(message)

    @classmethod
    def run(cls):
        """
        ClassMethod to parse the command line
        """
        cls.log("Running...")
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, *args):
        """
        Constructor of the winservice
        """
        self.log("Constructing Service")
        super().__init__(*args)
        self.server = Server()

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.log("ENTER SvcStop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        try:
            self.server.stop(self._stopped)
        except Exception as error:
            self.log_error(f"SvcStop {error}")

        self.log("EXIT SvcStop")

    def _stopped(self):
        self.log("ENTER _stopped")
        # # !important! to report "SERVICE_STOPPED"
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.log("EXIT _stopped")

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.log("ENTER SvcDoRun")

        self.server.run()

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )

        self.log("EXIT SvcDoRun")
