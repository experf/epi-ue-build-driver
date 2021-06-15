from __future__ import annotations
import logging

from servicemanager import LogInfoMsg, LogErrorMsg  # pylint: disable=import-error


class ServiceManagerLogHandler(logging.Handler):
    """
    A `logging.Handler` extension using [servicemanager][] logging methods

    [servicemanager]: http://timgolden.me.uk/pywin32-docs/servicemanager.html
    """

    @classmethod
    def singleton(cls) -> ServiceManagerLogHandler:
        instance = getattr(cls, "__singleton", None)
        if instance is not None and instance.__class__ == cls:
            return instance
        instance = cls()
        setattr(cls, "__singleton", instance)
        return instance

    # def __init__(self, level=logging.NOTSET):
    #     super().__init__(self, level=level)
    #     self.createLock()

    def emit(self, record):
        # pylint: disable=broad-except
        # self.acquire()
        LogInfoMsg("STARTING EMIT")
        try:
            message = self.format(record)
            if record.levelno in (logging.ERROR, logging.FATAL):
                LogErrorMsg(message)
            else:
                LogInfoMsg(message)
        except (KeyboardInterrupt, SystemExit) as error:
            # We want these guys to bub' up
            LogInfoMsg(f"EXIT {error}")
            # self.release()
            raise error
        except Exception as error:
            LogInfoMsg("HANDLING EMIT ERROR")
            LogInfoMsg(f"ERROR {error}")
            # self.release()
            # > handleError(record)
            # >
            # > This method should be called from handlers when an exception is
            # > encountered during an emit() call
            #
            # https://docs.python.org/3.9/library/logging.html#logging.Handler.handleError
            # self.handleError(record)
        # else:
        #     self.release()
