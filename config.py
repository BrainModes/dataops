import os
import requests
from requests.models import HTTPError
from pydantic import BaseSettings, Extra
from typing import Dict, Set, List, Any
from functools import lru_cache
from common import VaultClient
from dotenv import load_dotenv

load_dotenv()
SRV_NAMESPACE = os.environ.get("APP_NAME", "service_dataops_utility")
CONFIG_CENTER_ENABLED = os.environ.get("CONFIG_CENTER_ENABLED", "false")

def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    if CONFIG_CENTER_ENABLED == "false":
        return {}
    else:
        return vault_factory()


def vault_factory() -> dict:
    vc = VaultClient(os.getenv("VAULT_URL"), os.getenv("VAULT_CRT"), os.getenv("VAULT_TOKEN"))
    return vc.get_from_vault(SRV_NAMESPACE)


class Settings(BaseSettings):
    version = "0.1.0"

    port: int = 5063
    host: str = "127.0.0.1"
    env: str = ""
    namespace: str = ""
    OPEN_TELEMETRY_ENABLED: str

    GREENROOM_ZONE_LABEL: str = "Greenroom"
    CORE_ZONE_LABEL: str = "Core"

    AUTH_SERVICE: str
    NEO4J_SERVICE: str
    ENTITYINFO_SERVICE: str
    CATALOGUING_SERVICE: str
    QUEUE_SERVICE: str
    UTILITY_SERVICE: str
    SEND_MESSAGE_URL: str
    PROVENANCE_SERVICE: str
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_HTTPS: bool = False

    # Redis Service
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    REDIS_PASSWORD: str

    RDS_HOST: str
    RDS_PORT: str
    RDS_DBNAME: str
    RDS_USER: str
    RDS_PWD: str
    RDS_SCHEMA_DEFAULT: str

    def modify_values(self, settings):
        settings.AUTH_SERVICE = settings.AUTH_SERVICE + '/v1/'
        NEO4J_HOST = settings.NEO4J_SERVICE
        settings.NEO4J_SERVICE = NEO4J_HOST + "/v1/neo4j/"
        settings.NEO4J_SERVICE_V2 = NEO4J_HOST + "/v2/neo4j/"
        settings.ENTITYINFO_SERVICE = settings.ENTITYINFO_SERVICE + "/v1/"
        settings.CATALOGUING_SERVICE_V2 = settings.CATALOGUING_SERVICE + "/v2/"
        settings.QUEUE_SERVICE = settings.QUEUE_SERVICE + "/v1/"
        settings.UTILITY_SERVICE = settings.UTILITY_SERVICE
        settings.SEND_MESSAGE_URL = settings.SEND_MESSAGE_URL + "/v1/send_message"
        settings.PROVENANCE_SERVICE = settings.PROVENANCE_SERVICE + "/v1/"
        settings.MINIO_SERVICE = "http://" + settings.MINIO_ENDPOINT

        settings.disk_namespace = settings.namespace

        settings.REDIS_PORT = int(settings.REDIS_PORT)
        settings.REDIS_DB = int(settings.REDIS_DB)

        settings.SQLALCHEMY_DATABASE_URI = f"postgresql://{settings.RDS_USER}:{settings.RDS_PWD}@{settings.RDS_HOST}/{settings.RDS_DBNAME}"

        settings.opentelemetry_enabled = settings.OPEN_TELEMETRY_ENABLED == "TRUE"
        return settings

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                env_settings,
                load_vault_settings,
                init_settings,
                file_secret_settings,
            )


@lru_cache(1)
def get_settings():
    settings =  Settings()
    settings = settings.modify_values(settings)
    return settings

ConfigClass = get_settings()
