from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    CREATE TABLE IF NOT EXISTS "contact" (
        "id" UUID NOT NULL PRIMARY KEY,
        "first_name" VARCHAR(255),
        "last_name" VARCHAR(255),
        "note" TEXT
    );
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
