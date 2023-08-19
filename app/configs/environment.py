"""
Module to load all Environment variables
"""

from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    """
    Environment, add the variable and its type here matching the .env file
    """

    # RABBIT
    RBMQ_HOST: str
    RBMQ_USER: str
    RBMQ_PASS: str
    RBMQ_PORT: int
    RBMQ_EXCHANGE: str
    PREFETCH_VALUE: int

    # DATABASE
    DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    ENVIRONMENT: str
    DATABASE_MIN_CONNECTIONS: int
    DATABASE_MAX_CONNECTIONS: int

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: str
    TIMED_CACHE: int

    # QUEUES
    PROPERTY_IN_CHANNEL: str
    SAVE_PROPERTY_CHANNEL: str
    UPDATE_PROPERTY_CHANNEL: str
    INACTIVE_PROPERTY_CHANNEL: str
    PROPERTY_VALIDATOR_CHANNEL: str
    CHARACTERISTICS_CHANNEL: str
    PROPERTY_OUT_CHANNEL: str
    NEW_ADDRESS_CHANNEL: str

    # PORTAIS
    PORTAL_IMOVEIS_URL: str

    class Config:
        """Load config file"""

        env_file = ".env"
        extra='ignore'
