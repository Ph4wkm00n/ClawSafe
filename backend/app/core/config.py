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

    model_config = {"env_prefix": "CLAWSAFE_"}


settings = Settings()
