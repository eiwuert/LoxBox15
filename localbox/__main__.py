"""
Start the LocalBox server
"""
from localbox import main
from logging import DEBUG
from logging import StreamHandler, FileHandler
from logging.handlers import  SysLogHandler
from .config import prepare_logger
from .config import ConfigSingleton

if __name__ == '__main__':
    config = ConfigSingleton()
    logfile = config.get('logging', 'logfile')
    loghandlers = []
    if logfile is not None:
        loghandlers.append(FileHandler(logfile))
    if config.getboolean('logging', 'console', False):
        loghandlers.append(StreamHandler())
    syslog = config.get('logging', 'syslog', None)
    if syslog is not None:
        loghandlers.append(SysLogHandler(address=syslog))
    prepare_logger('database', DEBUG, loghandlers)
    prepare_logger('api', DEBUG, loghandlers)
    main()
