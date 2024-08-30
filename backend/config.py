import os

class Config:
    """
    Base configuration class. Contains default settings that can be 
    overridden by environment-specific configurations.
    """
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALEMBIC_INI_FILE = 'alembic.ini'

class DevelopmentConfig(Config):
    """
    Development configuration. Enables debug mode and uses a 
    development-specific database.
    """
    DEBUG = True
    DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')

class TestingConfig(Config):
    """
    Testing configuration. Uses a separate database for testing 
    purposes.
    """
    TESTING = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')

class ProductionConfig(Config):
    """
    Production configuration. Contains production-specific settings.
    """
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///prod.db')

# Dictionary to map environment names to configuration classes
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

def get_config(config_name):
    """
    Retrieves the configuration class based on the given environment name.

    Args:
        config_name (str): The environment name ('dev', 'test', 'prod').

    Returns:
        Config: The corresponding configuration class.
    """
    return config_by_name.get(config_name, Config)
