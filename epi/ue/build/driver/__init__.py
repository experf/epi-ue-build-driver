import sys

if sys.platform == "win32":
    from .win.win_service import WinService as Service
else:
    from .unix.service import Service

def main():
    Service.run()
