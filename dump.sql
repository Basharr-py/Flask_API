PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('de78ed3c412f');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(64) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(256), 
	name VARCHAR(120) NOT NULL, 
	avatar VARCHAR(256), bio VARCHAR(140), created_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO user VALUES(1,'Bash999','lateefazeez882@gmail.com','scrypt:32768:8:1$iv5tJJoKQ6USTjBo$cf32de8e0c8fdd899980c217cdf631ef501bb5b05b081c5c7a12653b08a17477061c37c5dcecf00f7c1beb3b9079d08528d89d97fd207615f40faafbd33bcbd4','Basharr Xzeez','https://ui-avatars.com/api/?name=Basharr+Xzeez&background=CC5500&color=fff','No Bio!!!','2025-12-31 22:28:19.774549');
INSERT INTO user VALUES(2,'Larry','lateefazeez88@gmail.com','scrypt:32768:8:1$0Rrbgxfs9m1Gy0Gp$e9e45c2b581c32670694319a6ffa66a3da549214873230ab057ceefd28cc64978d0d19b0276453eff7efa0c5c50776b01316507a25f3d638febb350ceacc7793','Olaonipekun','https://ui-avatars.com/api/?name=Olaonipekun&background=CC5500&color=fff',NULL,'2026-01-19 17:02:20.881693');
INSERT INTO user VALUES(3,'Basharr999','lateef882@gmail.com','scrypt:32768:8:1$3PwlT9cb1EaIS2DF$43c2e8784f1b6c9e8d9c019d32156c8ad14a8e9805a31b643f4406d71e6dee4d1e82a448f58889b3e9cb23b8ce136b3e233bd76d0981f75b6069fc993bc783f5','Abdullateef Olashile Azeez','https://ui-avatars.com/api/?name=Abdullateef+Olashile+Azeez&background=CC5500&color=fff','None','2026-08-09 02:14:02.054176');
INSERT INTO user VALUES(4,'bash','cfgyjioih@gmail.com','scrypt:32768:8:1$6aLui4R5AFc12FxU$e0bdb2c4fbf5ab30f112f69fa67fefd42fdf3f3ff364c961473b4c22f6cabf39bb2fdc26ea6b890caf77cff25f4d0c7161396217b5d0fcb7743e6fb96a74882b','Basha','https://ui-avatars.com/api/?name=Basha&background=CC5500&color=fff',NULL,'2026-09-22 00:57:20.199240');
CREATE TABLE post (
	id INTEGER NOT NULL, 
	body VARCHAR(140) NOT NULL, 
	timestamp DATETIME NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE IF NOT EXISTS "files" (
	id INTEGER NOT NULL, 
	course_code VARCHAR(200) NOT NULL, 
	status VARCHAR(200) NOT NULL, 
	credit_unit INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO files VALUES(1,'GNS 311','Required',2);
INSERT INTO files VALUES(2,'CSC 311 (AUTOMATA)','Core',2);
INSERT INTO files VALUES(3,'CSC 321','Required',2);
CREATE TABLE IF NOT EXISTS "materials" (
	id INTEGER NOT NULL, 
	filename VARCHAR(200) NOT NULL, 
	filepath VARCHAR(200) NOT NULL, 
	c_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(c_id) REFERENCES files (id)
);
INSERT INTO materials VALUES(1,'AUTOMATA THEORY lecture notes.pdf','uploads\AUTOMATA THEORY lecture notes.pdf',2);
INSERT INTO materials VALUES(2,'a1.pdf','uploads\a1.pdf',2);
INSERT INTO materials VALUES(3,'CSC 321 Number system.pdf','uploads\CSC 321 Number system.pdf',3);
CREATE UNIQUE INDEX ix_user_email ON user (email);
CREATE INDEX ix_user_name ON user (name);
CREATE UNIQUE INDEX ix_user_username ON user (username);
CREATE INDEX ix_post_timestamp ON post (timestamp);
CREATE INDEX ix_post_user_id ON post (user_id);
CREATE INDEX ix_materials_c_id ON materials (c_id);
COMMIT;
