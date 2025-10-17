from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from pymongo.collation import Collation


async def init_task_indexes(db: AsyncIOMotorDatabase) -> None:
    """
    Create indexes for the 'tasks' collection.
    """
    tasks = db["tasks"]

    # Unique title per owner (case-insensitive)
    await tasks.create_index(
        [("owner_id", ASCENDING), ("title", ASCENDING)],
        name="uniq_owner_title",
        unique=True,
        collation=Collation(locale="en", strength=2),
    )

    await tasks.create_index(
        [("created_at", DESCENDING)], name="idx_tasks_created_at"
    )
    await tasks.create_index(
        [("updated_at", DESCENDING)], name="idx_tasks_updated_at"
    )
    await tasks.create_index([("status", ASCENDING)], name="idx_tasks_status")
    await tasks.create_index(
        [("priority", ASCENDING)], name="idx_tasks_priority"
    )


async def init_user_indexes(db: AsyncIOMotorDatabase) -> None:
    """
    Create indexes for the 'users' collection.
    """
    users = db["users"]
    await users.create_index(
        [("username", ASCENDING)], unique=True, name="uniq_username",
        collation=Collation(locale="en", strength=2)
    )
    await users.create_index(
        [("email", ASCENDING)], unique=True, name="uniq_email",
        collation=Collation(locale="en", strength=2)
    )
    await users.create_index(
        [("created_at", DESCENDING)], name="idx_users_created_at"
    )


async def init_all_indexes(db: AsyncIOMotorDatabase) -> None:
    await init_user_indexes(db)
    await init_task_indexes(db)
