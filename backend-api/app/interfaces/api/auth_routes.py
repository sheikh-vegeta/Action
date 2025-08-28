from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.services.auth import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.models import User, Token, UserInDB

router = APIRouter()
auth_service = AuthService()


@router.post("/register", response_model=User)
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.get_user(form_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = auth_service.get_password_hash(form_data.password)
    user_in_db = UserInDB(username=form_data.username, hashed_password=hashed_password)
    return auth_service.create_user(user_in_db)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.get_user(form_data.username)
    if not user or not auth_service.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
