import win32serviceutil
import win32service
import win32event
import win32api
import subprocess
import os

class FlaskAppService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask Application Service"
    _svc_description_ = "Runs the Flask application as a Windows service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.hProcess = subprocess.Popen(['python', 'C:\\your\\path\\to_your_project_folder\\server.py'])

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.hProcess.terminate()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        while True:
            # Wait for the stop event
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                break

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FlaskAppService)
