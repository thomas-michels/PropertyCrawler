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

    # DATABASE
    DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_MIN_CONNECTIONS: int
    DATABASE_MAX_CONNECTIONS: int

    # QUEUES
    PROPERTY_IN_CHANNEL: str
    SAVE_PROPERTY_CHANNEL: str
    UPDATE_PROPERTY_CHANNEL: str
    INACTIVE_PROPERTY_CHANNEL: str

    class Config:
        """Load config file"""

        env_file = ".env"
