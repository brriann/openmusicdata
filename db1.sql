create table if not exists table1 (
    column1 int,
    column2 varchar(40)
);

insert into table1 (column1, column2) values (1, 'asdf')
insert into table1 (column1, column2) values (2, 'qwer')
insert into table1 (column1, column2) values (3, 'zxcv')


select * from table1
