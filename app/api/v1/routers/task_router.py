from fastapi import APIRouter, status, Depends, Response, Request

from app.api.dependencies import get_task_repository, get_current_user
from app.models.user_model import UserModel
from app.repositories.task_repository import TaskRepository, TaskId
from app.schemas.task_schema import (
    TaskCreate, TaskResponse, TaskList, TaskQueryParams, TaskPutUpdate,
    TaskPatchUpdate, PageMeta
)
from app.services.task_service import TaskService

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
async def create_task(
    task_data: TaskCreate,
    request: Request,
    response: Response,
    repository: TaskRepository = Depends(get_task_repository),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    task = await TaskService.create_task(
        owner_id=current_user.id or "", task_data=task_data,
        repository=repository
    )
    response.headers["Location"] = str(
        request.url_for("get_task", task_id=task.id)
    )
    return TaskResponse.model_validate(task)


@router.get(
    "/{task_id}",
    name="get_task",
    response_model=TaskResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
)
async def get_task(
    task_id: TaskId,
    repository: TaskRepository = Depends(get_task_repository),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    task = await TaskService.get_task(
        task_id, owner_id=current_user.id or "", repository=repository
    )
    return TaskResponse.model_validate(task)


@router.get(
    "/",
    response_model=TaskList,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    summary="List tasks",
)
async def list_tasks(
    params: TaskQueryParams = Depends(),
    repository: TaskRepository = Depends(get_task_repository),
    current_user: UserModel = Depends(get_current_user),
) -> TaskList:
    items, total = await TaskService.list_tasks(
        owner_id=current_user.id or "", params=params, repository=repository
    )
    return TaskList(
        items=[TaskResponse.model_validate(t) for t in items],
        meta=PageMeta(
            total=total, limit=params.limit, skip=params.skip,
            sort=params.sort, sort_dir=params.sort_dir
        ),
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    summary="Replace task by ID",
)
async def replace_task(
    task_id: TaskId,
    data: TaskPutUpdate,
    repository: TaskRepository = Depends(get_task_repository),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    task = await TaskService.replace_task(
        task_id, owner_id=current_user.id or "", data=data,
        repository=repository
    )
    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    summary="Patch task by ID",
)
async def patch_task(
    task_id: TaskId,
    data: TaskPatchUpdate,
    repository: TaskRepository = Depends(get_task_repository),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    payload = {k: v for k, v in data.model_dump(exclude_unset=True).items()}
    task = await TaskService.patch_task(
        task_id, owner_id=current_user.id or "", data=payload,
        repository=repository
    )
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task by ID",
)
async def delete_task(
    task_id: TaskId,
    repository: TaskRepository = Depends(get_task_repository),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    await TaskService.delete_task(
        task_id, owner_id=current_user.id or "", repository=repository
    )
    return None
