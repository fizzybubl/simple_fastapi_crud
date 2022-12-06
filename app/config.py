from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "127.0.0.1"
    database_port: str = "3306"
    database_password: str = "1234"
    database_user: str = "root"
    database_name: str = "python"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    token_timeout: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
