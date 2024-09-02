DROP TYPE IF EXISTS Connection_Type CASCADE;
CREATE TYPE Connection_Type AS ENUM (
    'Follow',
    'Connect',
    'Friend',
    'Like'
);

DROP TYPE IF EXISTS Reaction_Type CASCADE;
CREATE TYPE Reaction_Type AS ENUM (
    'Like',
    'Love', 
    'Care/Support', 
    'Haha', 
    'Wow', 
    'Sad',
    'Angry',
    'Celebrate',
    'Insightful',
    'Funny',
    'Dislike'
);

DROP TYPE IF EXISTS References_Type CASCADE;
CREATE TYPE References_Type AS ENUM (
    'Share',
    'Reply',
    'Quote'
);

DROP TYPE IF EXISTS Social_Media_Content_Type CASCADE;
CREATE TYPE Social_Media_Content_Type AS ENUM (
    'Post',
    'Comment'
);

DROP TABLE IF EXISTS Hashtag;
CREATE TABLE Hashtag (
    text TEXT PRIMARY KEY
);

DROP TABLE IF EXISTS Annotation;
CREATE TABLE Annotation (
    annotation_PK INT NOT NULL PRIMARY KEY,
    annotation TEXT
);

DROP TABLE IF EXISTS Social_Media_Content;
CREATE TABLE Social_Media_Content (
    URL TEXT,
    id TEXT PRIMARY KEY,
    social_media_content_type Social_Media_Content_Type,
    fk_annotation_annotation_PK INT,
    text TEXT,
    share_count INT,
    quote_count INT,
    like_count INT,
    reply_count INT
);

ALTER TABLE Social_Media_Content ADD CONSTRAINT FK_Social_Media_Content_2
    FOREIGN KEY (fk_annotation_annotation_PK)
    REFERENCES Annotation (annotation_PK)
    ON DELETE NO ACTION;

DROP TABLE IF EXISTS References_Table;
CREATE TABLE References_Table (
    fk_social_media_content_1 TEXT,
    fk_social_media_content_2 TEXT,
    type References_Type
);

ALTER TABLE References_Table ADD CONSTRAINT FK_References_Table_1
    FOREIGN KEY (fk_social_media_content_1)
    REFERENCES Social_Media_Content (id);
 
ALTER TABLE References_Table ADD CONSTRAINT FK_References_Table_2
    FOREIGN KEY (fk_social_media_content_2)
    REFERENCES Social_Media_Content (id);

DROP TABLE IF EXISTS Media;
CREATE TABLE Media (
    fk_Social_Media_Content_PK TEXT,
    id TEXT,
    metadata TEXT,
    URL TEXT,
    PRIMARY KEY (fk_Social_Media_Content_PK, id)
);

ALTER TABLE Media ADD CONSTRAINT Media_2
    FOREIGN KEY (fk_Social_Media_Content_PK)
    REFERENCES Social_Media_Content (id)
    ON DELETE NO ACTION;

DROP TABLE IF EXISTS Grupo;
CREATE TABLE Grupo (
    picture TEXT,
    URL TEXT,
    name TEXT,
    id TEXT PRIMARY KEY
);

DROP TABLE IF EXISTS Account;
CREATE TABLE Account (
    platform TEXT,
    URL TEXT,
    picture TEXT,
    name TEXT,
    id TEXT,
    fk_annotation_annotation_PK INT,
    account_name TEXT,
    bio TEXT,
    verified BOOLEAN,
    following INT,
    followers INT,
    PRIMARY KEY (platform, id)
);

ALTER TABLE Account ADD CONSTRAINT FK_Account_2
    FOREIGN KEY (fk_annotation_annotation_PK)
    REFERENCES annotation (annotation_PK)
    ON DELETE NO ACTION;

DROP TABLE IF EXISTS Connects;
CREATE TABLE Connects (
    fk_Account_platform_1 TEXT,
    fk_Account_id_1 TEXT,
    fk_Account_platform_2 TEXT,
    fk_Account_id_2 TEXT,
    type Connection_Type,
    PRIMARY KEY (fk_Account_platform_1, fk_Account_id_1, fk_Account_platform_2, fk_Account_id_2, type)
);

ALTER TABLE Connects ADD CONSTRAINT FK_Connects_1
    FOREIGN KEY (fk_Account_platform_1, fk_Account_id_1)
    REFERENCES Account (platform, id)
    ON DELETE CASCADE;
 
ALTER TABLE Connects ADD CONSTRAINT FK_Connects_2
    FOREIGN KEY (fk_Account_platform_2, fk_Account_id_2)
    REFERENCES Account (platform, id)
    ON DELETE CASCADE;

DROP TABLE IF EXISTS Belongs_To;
CREATE TABLE Belongs_To (
    fk_Social_Media_Content_id TEXT,
    fk_Grupo_id TEXT
);

ALTER TABLE Belongs_To ADD CONSTRAINT FK_Belongs_To_1
    FOREIGN KEY (fk_Social_Media_Content_id)
    REFERENCES Social_Media_Content (id)
    ON DELETE SET NULL;
 
ALTER TABLE Belongs_To ADD CONSTRAINT FK_Belongs_To_2
    FOREIGN KEY (fk_Grupo_id)
    REFERENCES Grupo (id)
    ON DELETE SET NULL;

DROP TABLE IF EXISTS Contains;
CREATE TABLE Contains (
    fk_Social_Media_Content_id TEXT,
    fk_Hashtag_text TEXT
);

ALTER TABLE Contains ADD CONSTRAINT FK_Contains_1
    FOREIGN KEY (fk_Social_Media_Content_id)
    REFERENCES Social_Media_Content (id)
    ON DELETE RESTRICT;
 
ALTER TABLE Contains ADD CONSTRAINT FK_Contains_2
    FOREIGN KEY (fk_Hashtag_text)
    REFERENCES Hashtag (text)
    ON DELETE SET NULL;

DROP TABLE IF EXISTS Mentions;
CREATE TABLE Mentions (
    fk_Social_Media_Content_id TEXT,
    fk_Account_platform TEXT,
    fk_Account_id TEXT
);

ALTER TABLE Mentions ADD CONSTRAINT FK_Mentions_1
    FOREIGN KEY (fk_Social_Media_Content_id)
    REFERENCES Social_Media_Content (id)
    ON DELETE SET NULL;
 
ALTER TABLE Mentions ADD CONSTRAINT FK_Mentions_2
    FOREIGN KEY (fk_Account_platform, fk_Account_id)
    REFERENCES Account (platform, id)
    ON DELETE SET NULL;

DROP TABLE IF EXISTS Belongs_To_Timeline;
CREATE TABLE Belongs_To_Timeline (
    fk_Account_platform TEXT,
    fk_Account_id TEXT,
    fk_Social_Media_Content_id TEXT
);

ALTER TABLE Belongs_To_Timeline ADD CONSTRAINT FK_Belongs_To_Timeline_1
    FOREIGN KEY (fk_Account_platform, fk_Account_id)
    REFERENCES Account (platform, id)
    ON DELETE SET NULL;
 
ALTER TABLE Belongs_To_Timeline ADD CONSTRAINT FK_Belongs_To_Timeline_2
    FOREIGN KEY (fk_Social_Media_Content_id)
    REFERENCES Social_Media_Content (id)
    ON DELETE SET NULL;

DROP TABLE IF EXISTS Creates;
CREATE TABLE Creates (
    fk_Account_platform TEXT,
    fk_Account_id TEXT,
    fk_Social_Media_Content_id TEXT,
    timestamp TIMESTAMP
);

ALTER TABLE Creates ADD CONSTRAINT FK_Creates_1
    FOREIGN KEY (fk_Account_platform, fk_Account_id)
    REFERENCES Account (platform, id)
    ON DELETE RESTRICT;
 
ALTER TABLE Creates ADD CONSTRAINT FK_Creates_2
    FOREIGN KEY (fk_Social_Media_Content_id)
    REFERENCES Social_Media_Content (id)
    ON DELETE SET NULL;

DROP TABLE IF EXISTS Reacts;
CREATE TABLE Reacts (
    fk_Social_Media_Content_id TEXT,
    fk_Account_platform TEXT,
    fk_Account_id TEXT,
    type Reaction_Type
);

ALTER TABLE Reacts ADD CONSTRAINT FK_Reacts_1
    FOREIGN KEY (fk_Social_Media_Content_id)
    REFERENCES Social_Media_Content (id)
    ON DELETE SET NULL;
 
ALTER TABLE Reacts ADD CONSTRAINT FK_Reacts_2
    FOREIGN KEY (fk_Account_platform, fk_Account_id)
    REFERENCES Account (platform, id)
    ON DELETE SET NULL;

DROP TABLE IF EXISTS Follows;
CREATE TABLE Follows (
    fk_Hashtag_text TEXT,
    fk_Account_platform TEXT,
    fk_Account_id TEXT
);

ALTER TABLE Follows ADD CONSTRAINT FK_Follows_1
    FOREIGN KEY (fk_Hashtag_text)
    REFERENCES Hashtag (text)
    ON DELETE SET NULL;
 
ALTER TABLE Follows ADD CONSTRAINT FK_Follows_2
    FOREIGN KEY (fk_Account_platform, fk_Account_id)
    REFERENCES Account (platform, id)
    ON DELETE SET NULL;

DROP TABLE IF EXISTS Participates;
CREATE TABLE Participates (
    fk_Account_platform TEXT,
    fk_Account_id TEXT,
    fk_Grupo_id TEXT,
    role TEXT
);
 
ALTER TABLE Participates ADD CONSTRAINT FK_Participates_1
    FOREIGN KEY (fk_Account_platform, fk_Account_id)
    REFERENCES Account (platform, id)
    ON DELETE RESTRICT;
 
ALTER TABLE Participates ADD CONSTRAINT FK_Participates_2
    FOREIGN KEY (fk_Grupo_id)
    REFERENCES Grupo (id)
    ON DELETE SET NULL;