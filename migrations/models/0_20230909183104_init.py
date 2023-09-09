from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "team" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL,
    "description" TEXT,
    "captain_id" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "student_email" VARCHAR(32)  UNIQUE,
    "login" VARCHAR(64) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(64) NOT NULL,
    "photo" VARCHAR(128),
    "role" VARCHAR(32),
    "team_id" INT,
    "cv" TEXT,
    "academic_group" VARCHAR(32)
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
