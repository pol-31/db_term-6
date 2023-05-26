-- location
CREATE TABLE IF NOT EXISTS tbl_zno_region (
    id serial PRIMARY KEY,
    reg char(30) NULL,
    area char(50) NULL,
    ter char(40) NULL,
    CONSTRAINT region_unique UNIQUE (reg, area, ter)
);

-- student's registration location
CREATE TABLE IF NOT EXISTS tbl_zno_reg_region (
    id serial PRIMARY KEY,
    ter_type char(5) NULL,
    fk_region int REFERENCES tbl_zno_region (id),
    CONSTRAINT reg_reg_unique UNIQUE (ter_type, fk_region)
);

-- student's educational institution
CREATE TABLE IF NOT EXISTS tbl_zno_eo (
    id serial PRIMARY KEY,
    name varchar(300) NULL,
    type char(60) NULL,
    parent varchar(300) NULL,
    fk_region int REFERENCES tbl_zno_region (id),
    CONSTRAINT eo_unique UNIQUE (name, type, parent)
);

-- zno venue
CREATE TABLE IF NOT EXISTS tbl_zno_pt (
    id serial PRIMARY KEY,
    name varchar(300) UNIQUE,
    fk_region int REFERENCES tbl_zno_region (id)
);


-- main student's table
CREATE TABLE IF NOT EXISTS tbl_zno_student (
    id char(36) PRIMARY KEY,
    birth int2 NOT NULL,
    sex char(10) NULL,
    status varchar(120) NULL,
    class_profile char(40) NULL,
    class_lang char(10) NULL,
    fk_student_reg int REFERENCES tbl_zno_reg_region (id),
    fk_eo int REFERENCES tbl_zno_eo (id)
);


CREATE TABLE IF NOT EXISTS tbl_zno_subject (
    id serial PRIMARY KEY,
    name char(20) UNIQUE
);

CREATE TABLE IF NOT EXISTS tbl_zno_marks (
    fk_student_id char(36) REFERENCES tbl_zno_student (id) NOT NULL,
    fk_subject int REFERENCES tbl_zno_subject (id) NOT NULL,
    fk_pt int REFERENCES tbl_zno_pt (id) NULL,
    test char(30) NULL,
    test_status char(20) NULL,
    ball100 decimal NULL,
    ball12 int2 NULL,
    ball int2 NULL,
    adapt_scale int2 NULL,
    lang char(10) DEFAULT 'українська',
    dpa char(30) NULL,
    PRIMARY KEY (fk_student_id, fk_subject)
);


