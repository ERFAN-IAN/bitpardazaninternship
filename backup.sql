/*
 Navicat Premium Dump SQL

 Source Server         : test1
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 04/05/2025 13:37:34
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for app_author
-- ----------------------------
DROP TABLE IF EXISTS "app_author";
CREATE TABLE "app_author" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar(100) NOT NULL,
  "last_name" varchar(100) NOT NULL,
  "age" integer unsigned NOT NULL,
  "national_id" varchar(10) NOT NULL,
  UNIQUE ("national_id" ASC),
   ("age" >= 0)
);

-- ----------------------------
-- Records of app_author
-- ----------------------------
INSERT INTO "app_author" VALUES (1, 'Rebecca', 'Yarros', 50, '545643245');
INSERT INTO "app_author" VALUES (2, 'George', 'Raymond Martin', 76, '545643638');
INSERT INTO "app_author" VALUES (6, 'dgdgf', 'frsfgdfgd', 120, '123123');

-- ----------------------------
-- Table structure for app_book
-- ----------------------------
DROP TABLE IF EXISTS "app_book";
CREATE TABLE "app_book" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "title" varchar(200) NOT NULL,
  "publication_year" integer unsigned NOT NULL,
  "author_id" bigint NOT NULL,
  FOREIGN KEY ("author_id") REFERENCES "app_author" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
   ("publication_year" >= 0)
);

-- ----------------------------
-- Records of app_book
-- ----------------------------
INSERT INTO "app_book" VALUES (2, 'onyx storm', 2025, 1);
INSERT INTO "app_book" VALUES (3, 'test', 2000, 1);
INSERT INTO "app_book" VALUES (8, 'dfsggdfs', 2022, 6);
INSERT INTO "app_book" VALUES (9, 'some', 1990, 1);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "auth_group";
CREATE TABLE "auth_group" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" varchar(150) NOT NULL,
  UNIQUE ("name" ASC)
);

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS "auth_group_permissions";
CREATE TABLE "auth_group_permissions" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "group_id" integer NOT NULL,
  "permission_id" integer NOT NULL,
  FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS "auth_permission";
CREATE TABLE "auth_permission" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "content_type_id" integer NOT NULL,
  "codename" varchar(100) NOT NULL,
  "name" varchar(255) NOT NULL,
  FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO "auth_permission" VALUES (1, 1, 'add_author', 'Can add author');
INSERT INTO "auth_permission" VALUES (2, 1, 'change_author', 'Can change author');
INSERT INTO "auth_permission" VALUES (3, 1, 'delete_author', 'Can delete author');
INSERT INTO "auth_permission" VALUES (4, 1, 'view_author', 'Can view author');
INSERT INTO "auth_permission" VALUES (5, 2, 'add_book', 'Can add book');
INSERT INTO "auth_permission" VALUES (6, 2, 'change_book', 'Can change book');
INSERT INTO "auth_permission" VALUES (7, 2, 'delete_book', 'Can delete book');
INSERT INTO "auth_permission" VALUES (8, 2, 'view_book', 'Can view book');
INSERT INTO "auth_permission" VALUES (9, 3, 'add_logentry', 'Can add log entry');
INSERT INTO "auth_permission" VALUES (10, 3, 'change_logentry', 'Can change log entry');
INSERT INTO "auth_permission" VALUES (11, 3, 'delete_logentry', 'Can delete log entry');
INSERT INTO "auth_permission" VALUES (12, 3, 'view_logentry', 'Can view log entry');
INSERT INTO "auth_permission" VALUES (13, 4, 'add_permission', 'Can add permission');
INSERT INTO "auth_permission" VALUES (14, 4, 'change_permission', 'Can change permission');
INSERT INTO "auth_permission" VALUES (15, 4, 'delete_permission', 'Can delete permission');
INSERT INTO "auth_permission" VALUES (16, 4, 'view_permission', 'Can view permission');
INSERT INTO "auth_permission" VALUES (17, 5, 'add_group', 'Can add group');
INSERT INTO "auth_permission" VALUES (18, 5, 'change_group', 'Can change group');
INSERT INTO "auth_permission" VALUES (19, 5, 'delete_group', 'Can delete group');
INSERT INTO "auth_permission" VALUES (20, 5, 'view_group', 'Can view group');
INSERT INTO "auth_permission" VALUES (21, 6, 'add_user', 'Can add user');
INSERT INTO "auth_permission" VALUES (22, 6, 'change_user', 'Can change user');
INSERT INTO "auth_permission" VALUES (23, 6, 'delete_user', 'Can delete user');
INSERT INTO "auth_permission" VALUES (24, 6, 'view_user', 'Can view user');
INSERT INTO "auth_permission" VALUES (25, 7, 'add_contenttype', 'Can add content type');
INSERT INTO "auth_permission" VALUES (26, 7, 'change_contenttype', 'Can change content type');
INSERT INTO "auth_permission" VALUES (27, 7, 'delete_contenttype', 'Can delete content type');
INSERT INTO "auth_permission" VALUES (28, 7, 'view_contenttype', 'Can view content type');
INSERT INTO "auth_permission" VALUES (29, 8, 'add_session', 'Can add session');
INSERT INTO "auth_permission" VALUES (30, 8, 'change_session', 'Can change session');
INSERT INTO "auth_permission" VALUES (31, 8, 'delete_session', 'Can delete session');
INSERT INTO "auth_permission" VALUES (32, 8, 'view_session', 'Can view session');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS "auth_user";
CREATE TABLE "auth_user" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "password" varchar(128) NOT NULL,
  "last_login" datetime,
  "is_superuser" bool NOT NULL,
  "username" varchar(150) NOT NULL,
  "last_name" varchar(150) NOT NULL,
  "email" varchar(254) NOT NULL,
  "is_staff" bool NOT NULL,
  "is_active" bool NOT NULL,
  "date_joined" datetime NOT NULL,
  "first_name" varchar(150) NOT NULL,
  UNIQUE ("username" ASC)
);

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO "auth_user" VALUES (1, 'pbkdf2_sha256$1000000$EQ4Jv3KjpMsoAi5fg5kN6c$OJ68fVDaKpVULoGH5Z4D1JFoOC/27xF6PLcl11cmuok=', '2025-04-21 12:07:23.723898', 1, 'erfan', '', '', 1, 1, '2025-04-21 12:07:07.787946', '');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_groups";
CREATE TABLE "auth_user_groups" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "user_id" integer NOT NULL,
  "group_id" integer NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_user_permissions";
CREATE TABLE "auth_user_user_permissions" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "user_id" integer NOT NULL,
  "permission_id" integer NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS "django_admin_log";
CREATE TABLE "django_admin_log" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "object_id" text,
  "object_repr" varchar(200) NOT NULL,
  "action_flag" smallint unsigned NOT NULL,
  "change_message" text NOT NULL,
  "content_type_id" integer,
  "user_id" integer NOT NULL,
  "action_time" datetime NOT NULL,
  FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
   ("action_flag" >= 0)
);

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO "django_admin_log" VALUES (1, '2', 'George Raymond Martin', 1, '[{"added": {}}]', 1, 1, '2025-04-21 12:08:52.866768');
INSERT INTO "django_admin_log" VALUES (2, '1', 'Onyx Storm', 1, '[{"added": {}}]', 2, 1, '2025-04-21 14:13:20.913552');
INSERT INTO "django_admin_log" VALUES (3, '2', 'onyx storm', 1, '[{"added": {}}]', 2, 1, '2025-04-21 14:42:03.526987');

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "django_content_type";
CREATE TABLE "django_content_type" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "app_label" varchar(100) NOT NULL,
  "model" varchar(100) NOT NULL
);

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO "django_content_type" VALUES (1, 'app', 'author');
INSERT INTO "django_content_type" VALUES (2, 'app', 'book');
INSERT INTO "django_content_type" VALUES (3, 'admin', 'logentry');
INSERT INTO "django_content_type" VALUES (4, 'auth', 'permission');
INSERT INTO "django_content_type" VALUES (5, 'auth', 'group');
INSERT INTO "django_content_type" VALUES (6, 'auth', 'user');
INSERT INTO "django_content_type" VALUES (7, 'contenttypes', 'contenttype');
INSERT INTO "django_content_type" VALUES (8, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS "django_migrations";
CREATE TABLE "django_migrations" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "app" varchar(255) NOT NULL,
  "name" varchar(255) NOT NULL,
  "applied" datetime NOT NULL
);

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO "django_migrations" VALUES (1, 'contenttypes', '0001_initial', '2025-04-21 11:53:22.681552');
INSERT INTO "django_migrations" VALUES (2, 'auth', '0001_initial', '2025-04-21 11:53:22.743205');
INSERT INTO "django_migrations" VALUES (3, 'admin', '0001_initial', '2025-04-21 11:53:22.778154');
INSERT INTO "django_migrations" VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-04-21 11:53:22.813499');
INSERT INTO "django_migrations" VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-21 11:53:22.839154');
INSERT INTO "django_migrations" VALUES (6, 'app', '0001_initial', '2025-04-21 11:53:22.867290');
INSERT INTO "django_migrations" VALUES (7, 'contenttypes', '0002_remove_content_type_name', '2025-04-21 11:53:22.959168');
INSERT INTO "django_migrations" VALUES (8, 'auth', '0002_alter_permission_name_max_length', '2025-04-21 11:53:22.994761');
INSERT INTO "django_migrations" VALUES (9, 'auth', '0003_alter_user_email_max_length', '2025-04-21 11:53:23.029065');
INSERT INTO "django_migrations" VALUES (10, 'auth', '0004_alter_user_username_opts', '2025-04-21 11:53:23.056268');
INSERT INTO "django_migrations" VALUES (11, 'auth', '0005_alter_user_last_login_null', '2025-04-21 11:53:23.091304');
INSERT INTO "django_migrations" VALUES (12, 'auth', '0006_require_contenttypes_0002', '2025-04-21 11:53:23.098267');
INSERT INTO "django_migrations" VALUES (13, 'auth', '0007_alter_validators_add_error_messages', '2025-04-21 11:53:23.122936');
INSERT INTO "django_migrations" VALUES (14, 'auth', '0008_alter_user_username_max_length', '2025-04-21 11:53:23.163502');
INSERT INTO "django_migrations" VALUES (15, 'auth', '0009_alter_user_last_name_max_length', '2025-04-21 11:53:23.196835');
INSERT INTO "django_migrations" VALUES (16, 'auth', '0010_alter_group_name_max_length', '2025-04-21 11:53:23.229309');
INSERT INTO "django_migrations" VALUES (17, 'auth', '0011_update_proxy_permissions', '2025-04-21 11:53:23.258647');
INSERT INTO "django_migrations" VALUES (18, 'auth', '0012_alter_user_first_name_max_length', '2025-04-21 11:53:23.293960');
INSERT INTO "django_migrations" VALUES (19, 'sessions', '0001_initial', '2025-04-21 11:53:23.312430');
INSERT INTO "django_migrations" VALUES (20, 'app', '0002_alter_author_age_alter_book_publication_year', '2025-04-21 15:34:13.978127');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "django_session";
CREATE TABLE "django_session" (
  "session_key" varchar(40) NOT NULL,
  "session_data" text NOT NULL,
  "expire_date" datetime NOT NULL,
  PRIMARY KEY ("session_key")
);

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO "django_session" VALUES ('es8czzxxp53a3fl2jq6pw04e1ori9fud', '.eJxVjEEOwiAQRe_C2hCGdqC4dN8zkGEGpWpoUtqV8e7apAvd_vfef6lI21ri1vISJ1FnBer0uyXiR647kDvV26x5rusyJb0r-qBNj7Pk5-Vw_w4KtfKtrxwMDkNvGDOI87nrHXGXEIMFawAxeZM6Z70gcHAUHNoeLYIwCYh6fwC81TbX:1u6pvn:gzcFPbZ6tR7xQzZxFVmiX2wluxVl_7mCxJr_H7v_tRY', '2025-05-05 12:07:23.730771');

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

-- ----------------------------
-- Records of sqlite_sequence
-- ----------------------------
INSERT INTO "sqlite_sequence" VALUES ('django_migrations', 20);
INSERT INTO "sqlite_sequence" VALUES ('django_admin_log', 3);
INSERT INTO "sqlite_sequence" VALUES ('django_content_type', 8);
INSERT INTO "sqlite_sequence" VALUES ('auth_permission', 32);
INSERT INTO "sqlite_sequence" VALUES ('auth_group', 0);
INSERT INTO "sqlite_sequence" VALUES ('auth_user', 1);
INSERT INTO "sqlite_sequence" VALUES ('app_author', 6);
INSERT INTO "sqlite_sequence" VALUES ('app_book', 9);

-- ----------------------------
-- Auto increment value for app_author
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 6 WHERE name = 'app_author';

-- ----------------------------
-- Auto increment value for app_book
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 9 WHERE name = 'app_book';

-- ----------------------------
-- Indexes structure for table app_book
-- ----------------------------
CREATE INDEX "app_book_author_id_980d3e25"
ON "app_book" (
  "author_id" ASC
);

-- ----------------------------
-- Auto increment value for auth_group
-- ----------------------------

-- ----------------------------
-- Indexes structure for table auth_group_permissions
-- ----------------------------
CREATE INDEX "auth_group_permissions_group_id_b120cbf9"
ON "auth_group_permissions" (
  "group_id" ASC
);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq"
ON "auth_group_permissions" (
  "group_id" ASC,
  "permission_id" ASC
);
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e"
ON "auth_group_permissions" (
  "permission_id" ASC
);

-- ----------------------------
-- Auto increment value for auth_permission
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 32 WHERE name = 'auth_permission';

-- ----------------------------
-- Indexes structure for table auth_permission
-- ----------------------------
CREATE INDEX "auth_permission_content_type_id_2f476e4b"
ON "auth_permission" (
  "content_type_id" ASC
);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq"
ON "auth_permission" (
  "content_type_id" ASC,
  "codename" ASC
);

-- ----------------------------
-- Auto increment value for auth_user
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 1 WHERE name = 'auth_user';

-- ----------------------------
-- Indexes structure for table auth_user_groups
-- ----------------------------
CREATE INDEX "auth_user_groups_group_id_97559544"
ON "auth_user_groups" (
  "group_id" ASC
);
CREATE INDEX "auth_user_groups_user_id_6a12ed8b"
ON "auth_user_groups" (
  "user_id" ASC
);
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq"
ON "auth_user_groups" (
  "user_id" ASC,
  "group_id" ASC
);

-- ----------------------------
-- Indexes structure for table auth_user_user_permissions
-- ----------------------------
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c"
ON "auth_user_user_permissions" (
  "permission_id" ASC
);
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b"
ON "auth_user_user_permissions" (
  "user_id" ASC
);
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq"
ON "auth_user_user_permissions" (
  "user_id" ASC,
  "permission_id" ASC
);

-- ----------------------------
-- Auto increment value for django_admin_log
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 3 WHERE name = 'django_admin_log';

-- ----------------------------
-- Indexes structure for table django_admin_log
-- ----------------------------
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb"
ON "django_admin_log" (
  "content_type_id" ASC
);
CREATE INDEX "django_admin_log_user_id_c564eba6"
ON "django_admin_log" (
  "user_id" ASC
);

-- ----------------------------
-- Auto increment value for django_content_type
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 8 WHERE name = 'django_content_type';

-- ----------------------------
-- Indexes structure for table django_content_type
-- ----------------------------
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq"
ON "django_content_type" (
  "app_label" ASC,
  "model" ASC
);

-- ----------------------------
-- Auto increment value for django_migrations
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 20 WHERE name = 'django_migrations';

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "django_session_expire_date_a5c62663"
ON "django_session" (
  "expire_date" ASC
);

PRAGMA foreign_keys = true;
