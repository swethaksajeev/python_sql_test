create database library_management;
use library_management;

create table books(book_id int primary key not null auto_increment,
					title varchar(30),
                    author varchar(30),
					category varchar(30),
                    total_copies int not null,
                    available_copies int not null);