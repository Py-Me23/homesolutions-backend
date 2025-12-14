# app/authz.py

from fastapi import Depends, HTTPException, status
from app.auth import authenticated_user  # ensure this is your async auth function

def has_roles(allowed_roles: list[str]):
    """
    Dependency generator to check if the authenticated user has one of the allowed roles.
    Usage: Depends(has_roles(["admin"])) or Depends(has_roles(["homeowner", "provider"]))
    """
    async def role_checker(user=Depends(authenticated_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{user['role']}' not authorized for this action",
            )
        return user

    return role_checker
