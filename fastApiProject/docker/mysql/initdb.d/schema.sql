CREATE TABLE  users (
    created VARCHAR(30),
    modified VARCHAR(30),
    user_id
)


CREATE TABLE articles (
art_seq INTEGER NOT NULL AUTO_INCREMENT,
title VARCHAR(100),
content VARCHAR(1000),
user_id CHAR(32),
PRIMARY KEY (artseq),
FOREIGN KEY(user_id) REFERENCES users (user_id)
)default = utf8mb4
