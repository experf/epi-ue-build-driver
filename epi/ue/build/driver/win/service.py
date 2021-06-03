# SEE https://devtut.github.io/python/creating-a-windows-service-using-python.html#running-a-flask-web-application-as-a-service

import socket
# from multiprocessing import Process

import win32serviceutil

import servicemanager
import win32event
import win32service

from epi.ue.build.driver.app import app


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
        # self.process = None
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        # !important! to report "SERVICE_STOPPED"
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        # self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # self.process.terminate()
        # self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        print("RUNNING!!!!")
        # self.process = Process(target=run_app)
        # self.process.start()
        # self.process.run()
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        app.run(port=5000)
