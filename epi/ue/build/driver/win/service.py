# pylint: disable=wrong-import-position,line-too-long

# References
# ============================================================================
#
# 1.    https://devtut.github.io/python/creating-a-windows-service-using-python.html#running-a-flask-web-application-as-a-service
# 2.    https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
#

import sys
if sys.platform != "win32":
    raise ImportError(
        f"{__name__} is windows-only (sys.platform={sys.platform}"
    )

import threading

import win32serviceutil # pylint: disable=import-error
import servicemanager # pylint: disable=import-error
import win32service # pylint: disable=import-error

from werkzeug.serving import make_server

from epi.ue.build.driver.app import app


class AppThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('STARTING server...')
        self.server.serve_forever()

    def shutdown(self):
        print('STOPING server...')
        self.server.shutdown()
        print('STOPPED server.')

class Service(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    _svc_name_ = "EPIUEBuildDriver"
    _svc_display_name_ = "EPI UE Build Driver"
    _svc_description_ = "Unreal Engine build driver"

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
        self.app_thread = None

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        print("ENTER SvcStop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.app_thread.shutdown()
        # # !important! to report "SERVICE_STOPPED"
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        print("EXIT SvcStop")

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        print("ENTER SvcDoRun")
        self.app_thread = AppThread()
        self.app_thread.start()
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.app_thread.join()
        print("EXIT SvcDoRun")
