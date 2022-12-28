create view analysis.view_orderitems as (select * from production.orderitems);

create view analysis.view_orders as (select * from production.orders); 

create view analysis.view_orderstatuses as (select * from production.orderstatuses); 

create view analysis.view_orderstatuslog as (select * from production.orderstatuslog); 

create view analysis.view_products as (select * from production.products); 

create view analysis.view_users as (select * from production.users); 
