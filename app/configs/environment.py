"""
Module to load all Environment variables
"""

from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    """
    Environment, add the variable and its type here matching the .env file
    """

    RBMQ_HOST: str
    RBMQ_USER: str
    RBMQ_PASS: str
    RBMQ_PORT: int
    RBMQ_EXCHANGE: str

    DATABASE_URL: str

    class Config:
        """Load config file"""

        env_file = ".env"
