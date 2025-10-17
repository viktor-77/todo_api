from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user_repository, get_current_user
from app.models.user_model import UserModel
from app.repositories.errors import UniqueViolationError, RepositoryError
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserCreate, UserPublic, Token
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register", response_model=UserPublic,
    status_code=status.HTTP_201_CREATED, summary="Register a new user"
)
async def register_user(data: UserCreate, repo: UserRepository = Depends(
    get_user_repository
)) -> UserPublic:
    try:
        user = await AuthService.register_user(data, repo)
    except UniqueViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )
    except RepositoryError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal error"
        )
    return UserPublic.model_validate(user)


@router.post(
    "/login", response_model=Token,
    summary="Obtain access token via username/password"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repository),
) -> Token:
    user = await AuthService.authenticate_user(
        form_data.username, form_data.password, repo
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = AuthService.mint_access_token(user.id or "")
    return Token(access_token=token)


@router.get(
    "/me", response_model=UserPublic, summary="Get current user profile"
)
async def me(
    current_user: UserModel = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)
