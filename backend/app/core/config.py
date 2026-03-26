from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ClawSafe"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    database_path: str = "clawsafe.db"
    openclaw_config_path: str = "/etc/openclaw/config.yaml"
    frontend_url: str = "http://localhost:3000"
    api_key: str = ""
    scan_interval: int = 3600
    demo_mode: bool = True
    log_level: str = "INFO"
    db_type: str = "sqlite"
    db_url: str = ""
    db_pool_min: int = 2
    db_pool_max: int = 10
    jwt_secret: str = ""
    jwt_expire_minutes: int = 1440
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""

    model_config = {"env_prefix": "CLAWSAFE_"}


settings = Settings()
