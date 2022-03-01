DROP TABLE IF EXISTS station;
DROP TABLE IF EXISTS trainline;
DROP TABLE IF EXISTS trainschedule;

CREATE TABLE "station" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "trainline" (
	"id"	TEXT NOT NULL,
	"stationid"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("stationid") REFERENCES "station"("id")
);

CREATE TABLE "trainschedule" (
	"id"	TEXT NOT NULL,
	"time"	INTEGER NOT NULL,
	FOREIGN KEY("id") REFERENCES "trainline"("id")
);