from typing import List
from fastapi import Header, HTTPException, status
from app.security import verify_token_and_get_roles


async def require_user_role(authorization: str = Header(None)) -> List[str]:
    """Проверка наличия роли USER"""
    roles = await verify_token_and_get_roles(authorization)

    if "USER" in roles or "ADMIN" in roles:
        return roles

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Токен валиден, но нет роли USER"
    )


async def require_admin_role(authorization: str = Header(None)) -> List[str]:
    """Проверка наличия роли ADMIN"""
    roles = await verify_token_and_get_roles(authorization)
    if "ADMIN" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Токен валиден, но нет роли ADMIN"
        )
    return roles

