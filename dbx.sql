-- Table users ----------------------------------
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    users_name TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    user_campaign_id INTEGER DEFAULT NULL,
    timex DATETIME NOT NULL,
    is_active BOOLEAN NOT NULL CHECK (is_active IN (0, 1))
);

-- used in the project
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    users_name TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    user_campaign_id INTEGER DEFAULT NULL,
    users_creation_datetime DATETIME NOT NULL,
    is_active INTEGER CHECK (is_active IN (0, 1))
); 

-- used in the project
CREATE TABLE responseSet (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        response TEXT NOT NULL,
        token TEXT NOT NULL,
        questionId INTEGER NOT NULL,
        is_active bit not null DEFAULT (1),
        timex DATETIME NOT NULL
);

-- questionset 
CREATE TABLE questionset (
	id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
	campaign_id INTEGER DEFAULT NULL,
	groupset_id INTEGER DEFAULT NULL,
	questionset_name TEXT NOT NULL,
	questionset_question TEXT NOT NULL,
	questionset_type_id INTEGER NOT NULL,
	questioet_user_owner TEXT,
	questionset_creation_datnsetime DATETIME NOT NULL,
	is_active INTEGER CHECK (is_active IN (0, 1))
);

INSERT INTO questionset (campaign_id, groupset_id, questionset_name, questionset_question, questionset_type_id,  questionset_user_owner, questionset_creation_datetime, is_active) VALUES ();
INSERT INTO questionset (questionset_name, questionset_question, questionset_type_id,  questionset_user_owner, questionset_creation_datetime, is_active) VALUES ("question set example 1", "have you been in japan?", 3,"sys", datetime('now'),1);

-- questiontype table ------------------------------------------------------
CREATE TABLE questiontype (
	id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
	questiontype_name TEXT NOT NULL,
	questiontype_user_owner TEXT,
	questiontype_creation_datetime DATETIME NOT NULL,
	is_active INTEGER CHECK (is_active IN (0, 1))
);

--  groupset used -----------------------------------------------------------
CREATE TABLE groupset (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    groupset_name TEXT NOT NULL UNIQUE,
    user_campaign_id INTEGER DEFAULT NULL,
    groupset_user_owner TEXT,
    groupset_creation_datetime DATETIME NOT NULL,
    is_active INTEGER CHECK (is_active IN (0, 1))
);

INSERT INTO groupset (groupset_name, groupset_user_owner, groupset_creation_datetime, is_active) VALUES ('?,?,?,?')

INSERT INTO questiontype (questiontype_name, questiontype_user_owner, questiontype_creation_datetime, is_active) VALUES ("checkbox", "sys", datetime('now'), 1)\

INSERT INTO questiontype VALUES(1,'checkbox','sys','2022-10-26 01:45:54',1);
INSERT INTO questiontype VALUES(2,'radio','sys','2022-10-26 01:46:33',1);
INSERT INTO questiontype VALUES(3,'bool','sys','2022-10-26 01:46:38',1);
INSERT INTO questiontype VALUES(4,'text','sys','2022-10-26 01:46:44',1);
INSERT INTO questiontype VALUES(5,'list','sys','2022-10-26 01:46:51',1);


CREATE TABLE set_question (
    -- id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    groupset_id INTEGER DEFAULT NULL,
    questionset_id INTEGER DEFAULT NULL
);
	 
	 
	 
CREATE TABLE campaign (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    username TEXT,
    timex DATETIME NOT NULL
    is_active
)

CREATE TABLE campaign (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    -- campaign_name INT NOT NULL AUTO_INCREMENT,
    campaign_name VARCHAR(30) NOT NULL UNIQUE,
    campaign_username_owner VARCHAR(30) NOT NULL,
    cell_phone VARCHAR(15),
    age INT DEFAULT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE sharesActual (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        symbol TEXT NOT NULL,
        symbolName TEXT NOT NULL,
        sharesActual INTEGER NOT NULL,
        sharesPrice NUMERIC NOT NULL
);
CREATE TABLE cashAvailable (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        cash NUMERIC(8,2) NOT NULL,
        cashAvailableTime DATETIME NOT NULL
);
CREATE TABLE sharesHistory (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        symbol TEXT NOT NULL,
        symbolName TEXT NOT NULL,
        sharesTransaction INTEGER NOT NULL,
        sharesPrice NUMERIC(8,2) NOT NULL,
        timex DATETIME NOT NULL
);

queryResult = db.execute("select qs.* from groupset as g left join set_question as sq on g.id = sq.groupset_id left join questionset as qs on qs.id = sq.questionset_id where g.id = ?;", groupsetResult[0]['GroupsetId'])
select groupset.id, groupset.groupset_name, survey_urls.urlname from groupset join survey_urls on survey_urls.GroupsetId = groupset.id where groupset.id = 1;
survey_urls.GroupsetId
survey_urls.urlname

-- Join
select responseSet.response, questionset.questionset_question
FROM responseSet
JOIN questionset
ON questionset.id = responseSet.questionId
GROUP BY questionset.id;

-- results:
select response, count(response), questionid from responseSet where questionid = 15 group by response;

-- results ok - script is working
select questionset.id, questionset.questionset_question, responseSet.response, count(responseSet.response),  responseSet.token
from questionset
join responseSet
on responseSet.questionId = questionset.id
where responseSet.questionid = 12
and responseSet.token = 'gz35y21e'
group by responseSet.response;

-- results 
select questionset.id, questionset.questionset_question, responseSet.response, count(responseSet.response),  responseSet.token
from questionset
left join responseSet
on responseSet.questionId = questionset.id
where responseSet.token = 'gz35y21e'
group by responseSet.response;

select questionset.id, questionset.questionset_question, responseSet.response, count(responseSet.response),  responseSet.token
from questionset
left join responseSet
on responseSet.questionId = questionset.id
where responseSet.token = 'gz35y21e'
group by responseSet.response order by 1;


select count(response) from responseSet where token = 'gz35y21e';

select questionId from responseSet group by questionId;


-- CREATE TABLE kk (
--     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
--     friend_id INT NOT NULL AUTO_INCREMENT,
--     first_name VARCHAR(30) NOT NULL,
--     last_name VARCHAR(30) NOT NULL,
--     cell_phone VARCHAR(15),
--     age INT DEFAULT NULL,
--     PRIMARY KEY (id)
-- );

-- PRAGMA foreign_keys=OFF;
-- BEGIN TRANSACTION;
-- CREATE TABLE sharesActual (
-- 	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
-- 	symbol TEXT NOT NULL,
-- 	symbolName TEXT NOT NULL,
-- 	sharesActual INTEGER NOT NULL,
-- 	sharesPrice NUMERIC NOT NULL
-- );
-- CREATE TABLE cashAvailable (
--         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--         cash NUMERIC(8,2) NOT NULL,
--         cashAvailableTime DATETIME NOT NULL
-- );
-- INSERT INTO cashAvailable VALUES(1,2052.8000000000001818,'2022-10-19 03:58:30');
-- CREATE TABLE sharesHistory (
--         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--         symbol TEXT NOT NULL,
--         symbolName TEXT NOT NULL,
--         sharesTransaction INTEGER NOT NULL,
--         sharesPrice NUMERIC(8,2) NOT NULL,
--         timex DATETIME NOT NULL
-- );
-- CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL UNIQUE, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
-- INSERT INTO users VALUES(1,'tampico','pbkdf2:sha256:260000$brCCpZIsYkV0QyV1$15fe89b627c854e076ac893d37afe063c563e43df09f847ef38dad9d1fa6138e',10000);
-- DELETE FROM sqlite_sequence;
-- INSERT INTO sqlite_sequence VALUES('cashAvailable',1);
-- INSERT INTO sqlite_sequence VALUES('sharesHistory',20);
-- INSERT INTO sqlite_sequence VALUES('users',15);
-- COMMIT;
-- update questionset set questionset_type_id = 'bool' where id = 1;
