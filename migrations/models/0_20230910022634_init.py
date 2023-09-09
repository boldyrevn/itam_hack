from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "hackathon" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "description" TEXT NOT NULL,
    "contacts" TEXT NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS "role" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "team" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL UNIQUE,
    "description" TEXT,
    "captain_id" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "group" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "status" VARCHAR(32) NOT NULL,
    "hackathon_id" BIGINT NOT NULL REFERENCES "hackathon" ("id") ON DELETE CASCADE,
    "team_id" BIGINT NOT NULL REFERENCES "team" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "student_email" VARCHAR(32)  UNIQUE,
    "login" VARCHAR(64) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(64) NOT NULL,
    "photo" VARCHAR(128),
    "cv" TEXT,
    "academic_group" VARCHAR(32),
    "team_id" BIGINT REFERENCES "team" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "group_user" (
    "group_id" BIGINT NOT NULL REFERENCES "group" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_role" (
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "role_id" INT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
