from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "message" (
            "id" UUID NOT NULL PRIMARY KEY,
            "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "message" TEXT NOT NULL,
            "sender" VARCHAR(255) NOT NULL,
            "date" VARCHAR(35) NOT NULL
        );
        CREATE INDEX IF NOT EXISTS "idx_message_created_1cd580" ON "message" ("created");
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
