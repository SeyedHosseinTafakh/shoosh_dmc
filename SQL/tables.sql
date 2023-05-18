use dmc;
drop table if exists users;
drop table if exists records ;
drop table if exists user_codes ;


create table users (
    uid varchar(250)  primary key,
    name varchar(250) not null,
    password varchar(250) not null
);

create table records (
    guid binary(16) default (uuid_to_bin(uuid())) not null primary key,
    p_name varchar(250) not null,
    p_phone_number varchar(250) not null,
    more_text TINYTEXT,
    file_dir varchar(250) not null,
    user_id varchar(250) not null,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	created_atj varchar(250)
);

create table user_codes(
	guid binary(16) default (uuid_to_bin(uuid())) not null primary key,
    p_phone_number varchar(250) not null,
    p_access_code varchar(250) not null 
);
