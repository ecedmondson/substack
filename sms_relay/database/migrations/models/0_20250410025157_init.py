from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "contact" (
    "id" UUID NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(255),
    "last_name" VARCHAR(255),
    "note" TEXT
);
CREATE TABLE IF NOT EXISTS "phonenumber" (
    "id" UUID NOT NULL PRIMARY KEY,
    "number" VARCHAR(15) NOT NULL,
    "contact_id" UUID NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
