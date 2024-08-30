import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'sqlalchemy.engine': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

def setup_logging():
    """
    Set up logging configuration using the predefined settings.
    """
    logging.config.dictConfig(LOGGING_CONFIG)
