CREATE TABLE "orgs" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "shortname" TEXT,
    "fullname" TEXT
);
CREATE TABLE "netblocks" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "block" TEXT,
    "owner" INTEGER
);
CREATE TABLE "ips" (
    "ip" INTEGER,
    "owner" INTEGER,
    "netblock" INTEGER
);