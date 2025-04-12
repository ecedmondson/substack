from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "forwarded_message" (
            "id" UUID NOT NULL PRIMARY KEY,
            "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "message" TEXT NOT NULL,
            "date" VARCHAR(35) NOT NULL,
            "contact_id" UUID NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS "idx_forwarded_m_created_fda6c2" ON "forwarded_message" ("created");
        DROP TABLE IF EXISTS "message";
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "forwarded_message";
    """
