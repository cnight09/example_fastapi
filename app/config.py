from pydantic import BaseSettings

# environment variables with type and default
class Settings(BaseSettings):
#  database_password: str = "def_localhost"
#  database_username: str = "def_postgres"
#  secret_key: str = "def_adsf347jaowr10"
  database_hostname: str
  database_port: str
  database_password: str
  database_name: str
  database_username: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int

  class Config:
      env_file = ".env"

# create instance of the settings class
settings = Settings()
