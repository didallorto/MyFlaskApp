CREATE DATABASE myflaskapp
use myflaskapp

CREATE TABLE users(
	id int identity(3,3)
	, name varchar(30)
	, email varchar(50)
	, username varchar(10)
	, [password] varchar(200)
	, register_date datetime not null
	, constraint pk_id primary key(id)
);
go

alter table users add register_date datetime not null 




INSERT dbo.users(name, email, username, [password], register_date)
    VALUES ('master1', 'iotontos@iotontos.com.br', '@masterbr', 999999, GETDATE())
GO  

INSERT INTO dbo.users( name, email, username, [password], register_date)
    VALUES ('master1''masterotontos@iotontos.com.br', '@masterbr1', 999999, GETDATE())
	go

INSERT INTO dbo.users( name, email, username, [password], register_date)
    VALUES ('flask', 'flask@sqlserver.db', 'flask', '@darkmater2019', GETDATE())
	go