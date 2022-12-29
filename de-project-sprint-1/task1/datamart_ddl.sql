create table analysis.tmp_rfm_recency (
user_id int not null primary key,
recency int not null check (recency >= 1 and recency <= 5));

create table analysis.tmp_rfm_frequency (
user_id int not null primary key,
frequency int not null check (frequency >= 1 and frequency <= 5));

create table analysis.tmp_rfm_monetary_value (
user_id int not null primary key,
monetary_value int not null check (monetary_value >= 1 and monetary_value <= 5));

create table analysis.dm_rfm_segments (
user_id int not null primary key,
recency int,
frequency int,
monetary_value int);
ывао
