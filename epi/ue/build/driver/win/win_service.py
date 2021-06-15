# pylint: disable=wrong-import-position,line-too-long

# References
# ============================================================================
#
# 1.    https://devtut.github.io/python/creating-a-windows-service-using-python.html#running-a-flask-web-application-as-a-service
# 2.    https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
#

import logging

# import sys
# if sys.platform != "win32":
#     raise ImportError(
#         f"{__name__} is windows-only (sys.platform={sys.platform}"
#     )

import win32serviceutil  # pylint: disable=import-error
import servicemanager  # pylint: disable=import-error
import win32service  # pylint: disable=import-error

from epi.ue.build.driver.server import Server
from .service_manager_log_handler import ServiceManagerLogHandler


LOG = logging.getLogger(__name__)


class WinService(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    # self.log.FORMATTER = logging.Formatter(
    #     "%(threadName)s %(levelname)s %(name)s %(message)s"
    # )
    # self.log.HANDLER = logging.FileHandler(
    #     Path("C:\\", "temp", "epi-ue-build-driver.log")
    # )
    # self.log.HANDLER.setFormatter(self.log.FORMATTER)

    _svc_name_ = "EPIUEBuildDriver"
    _svc_display_name_ = "EPI UE Build Driver"
    _svc_description_ = "Unreal Engine build driver"

    server: Server

    @classmethod
    def setup_logging(cls) -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[ServiceManagerLogHandler.singleton()],
            force=True,
        )

    @classmethod
    def run(cls):
        """
        ClassMethod to parse the command line
        """
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, *args):
        """
        Constructor of the winservice
        """
        super().__init__(*args)
        self.server = None

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        LOG.debug("ENTER SvcStop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.server.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        LOG.debug("EXIT SvcStop")

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.__class__.setup_logging()
        LOG.debug("ENTER SvcDoRun")

        self.server = Server()
        self.server.run()

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )

        LOG.debug("EXIT SvcDoRun")
