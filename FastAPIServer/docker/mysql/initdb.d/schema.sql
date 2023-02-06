'''CREATE TABLE articles (
artseq INTEGER NOT NULL AUTO_INCREMENT,
title VARCHAR(100),
content VARCHAR(1000),
userid CHAR(32),
PRIMARY KEY (artseq),
FOREIGN KEY(userid) REFERENCES users (userid)
)default = utf8mb4'''
