create table posts(
    post_id bigint auto_increment primary key,
    title varchar(20),
    content varchar(20),
    create_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime ON UPDATE CURRENT_TIMESTAMP
)charset = utf8;

create table users(
    user_email varchar(20) primary key,
    password varchar(20),
    user_name varchar(20),
    phone varchar(20),
    birth varchar(20),
    address varchar(20),
    job varchar(20),
    user_interests varchar(20),
    token varchar(20)
)charset = utf8;

