from typing import Optional, List
from fastapi import HTTPException, status
from .config import keycloak_openid, settings


async def get_idp_public_key() -> str:
    """Получает публичный ключ из Keycloak"""
    try:
        public_key = keycloak_openid.public_key()
        return (
            "-----BEGIN PUBLIC KEY-----\n"
            f"{public_key}"
            "\n-----END PUBLIC KEY-----"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Не удалось получить публичный ключ из Keycloak: {str(e)}"
        )


async def decode_token(token: str) -> dict:
    """Декодирует JWT токен с проверкой подписи"""
    try:
        public_key = await get_idp_public_key()
        payload = keycloak_openid.decode_token(
            token,
            key=public_key,
            options={
                "verify_signature": True,
                "verify_aud": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_iat": True,
                "verify_nbf": True,
                "audience": settings.keycloak_client_id
            },
            issuer=f"{settings.keycloak_public_url}/realms/{settings.keycloak_realm}"
        )
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Невалидный токен: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_roles(token_payload: dict) -> List[str]:
    """Извлечение ролей пользователя из токена"""
    roles = []

    if "realm_access" in token_payload:
        roles.extend(token_payload["realm_access"].get("roles", []))

    if "resource_access" in token_payload:
        for client, data in token_payload["resource_access"].items():
            roles.extend(data.get("roles", []))

    return roles


async def verify_token(authorization: Optional[str]) -> List[str]:
    """Проверяет токен"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Отсутствует заголовок Authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверная схема авторизации. Ожидается Bearer",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат заголовка Authorization",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


async def get_roles(authorization: Optional[str]) -> List[str]:
    """возвращает роли пользователя"""
    
    token = await verify_token(authorization)
    token_payload = await decode_token(token)
    roles = get_user_roles(token_payload)
    
    return roles
