use dmc;
drop table if exists users;
drop table if exists records ;

create table users (
    guid binary(16) default (uuid_to_bin(uuid())) not null primary key,
    name varchar(250) not null,
    password varchar(250) not null
);

create table records (
    guid binary(16) default (uuid_to_bin(uuid())) not null primary key,
    p_name varchar(250) not null,
    p_phone_number varchar(250) not null,
    file_dir varchar(250) not null,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);