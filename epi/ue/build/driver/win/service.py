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
import logging

import win32serviceutil # pylint: disable=import-error
import servicemanager # pylint: disable=import-error
import win32service # pylint: disable=import-error

from epi.ue.build.driver.server import Server

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

class Service(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    _svc_name_ = "EPIUEBuildDriver"
    _svc_display_name_ = "EPI UE Build Driver"
    _svc_description_ = "Unreal Engine build driver"

    server: Server

    @classmethod
    def run(cls):
        """
        ClassMethod to parse the command line
        """
        logging.basicConfig()
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, *args):
        """
        Constructor of the winservice
        """
        super().__init__(*args)
        self.server = Server()

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        print("ENTER SvcStop [Thread {threading.get_ident()}]")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        get_or_create_eventloop().run_until_complete(
            self.server.server.stop()
        )
        # # !important! to report "SERVICE_STOPPED"
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        print("EXIT SvcStop [Thread {threading.get_ident()}]")

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        print(f"ENTER SvcDoRun [Thread {threading.get_ident()}]")

        self.server.run()

        # servicemanager.LogMsg(
        #     servicemanager.EVENTLOG_INFORMATION_TYPE,
        #     servicemanager.PYS_SERVICE_STARTED,
        #     (self._svc_name_, ""),
        # )

        print(f"EXIT SvcDoRun [Thread {threading.get_ident()}]")
