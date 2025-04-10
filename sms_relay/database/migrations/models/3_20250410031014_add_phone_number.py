from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "phonenumber" (
            "id" UUID NOT NULL PRIMARY KEY,
            "number" VARCHAR(15) NOT NULL,
            "contact_id" UUID NOT NULL REFERENCES "contact" ("id") ON DELETE CASCADE
        );
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "contact";
    """
