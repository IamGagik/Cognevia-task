from pydantic_settings import BaseSettings
from keycloak import KeycloakOpenID


class Settings(BaseSettings):
    keycloak_url: str = "http://keycloak:8080"
    keycloak_public_url: str = "http://localhost:8080"
    keycloak_realm: str = "cognevia-realm"
    keycloak_client_id: str = "fastapi-client"
    keycloak_client_secret: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

keycloak_openid = KeycloakOpenID(
    server_url=settings.keycloak_url,
    client_id=settings.keycloak_client_id,
    realm_name=settings.keycloak_realm,
    client_secret_key=settings.keycloak_client_secret if settings.keycloak_client_secret else None,
    verify=True
)

