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
    CREATE TABLE IF NOT EXISTS "group" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "status" VARCHAR(32) NOT NULL,
    "hackathon_id" BIGINT NOT NULL REFERENCES "hackathon" ("id") ON DELETE CASCADE,
    "team_id" BIGINT NOT NULL REFERENCES "team" ("id") ON DELETE CASCADE
);
        ALTER TABLE "user" ALTER COLUMN "team_id" TYPE BIGINT USING "team_id"::BIGINT;
        CREATE UNIQUE INDEX "uid_team_name_545714" ON "team" ("name");
        CREATE TABLE "group_user" (
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "group_id" BIGINT NOT NULL REFERENCES "group" ("id") ON DELETE CASCADE
);
        ALTER TABLE "user" ADD CONSTRAINT "fk_user_team_10b71bb3" FOREIGN KEY ("team_id") REFERENCES "team" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP CONSTRAINT "fk_user_team_10b71bb3";
        DROP TABLE IF EXISTS "group_user";
        DROP INDEX "idx_team_name_545714";
        ALTER TABLE "user" ALTER COLUMN "team_id" TYPE INT USING "team_id"::INT;
        DROP TABLE IF EXISTS "group";
        DROP TABLE IF EXISTS "hackathon";"""
