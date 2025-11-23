from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from app.dependencies import require_user_role, require_admin_role


app = FastAPI(title="Keycloak JWT Auth API", version="1.0.0")


@app.get("/user/resource")
async def user_resource(roles: List[str] = Depends(require_user_role)):
    return {
        "message": "Ваш токен валиден и есть роль USER или ADMIN", 
        "roles": roles
    }


@app.get("/admin/resource")
async def admin_resource(roles: List[str] = Depends(require_admin_role)):
    return {
        "message": "Ваш токен валиден и есть роль ADMIN",
        "roles": roles
    }


@app.get("/any/resource")
async def any_resource(roles: List[str] = Depends(require_admin_role)):
    return {
        "message": "Ваш токен валиден и есть роль ADMIN",
        "roles": roles
    }

