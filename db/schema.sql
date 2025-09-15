CREATE TABLE group_member (
    group_id varchar,
    email varchar unique,
    github varchar unique,
    invite_id varchar unique,
    invite_status bool,
    PRIMARY KEY (group_id, email)
);

CREATE TABLE valid_email (
    email varchar PRIMARY KEY
);

CREATE SEQUENCE tmp_group_id START 1;
CREATE SEQUENCE group_id START 1;
