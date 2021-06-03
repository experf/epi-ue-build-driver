import sys

if sys.platform == "win32":
    from .win.service import Service
else:
    from .unix.service import Service

def main():
    Service.run()
