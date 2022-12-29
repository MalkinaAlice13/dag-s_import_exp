CREATE OR REPLACE view analysis.view_orderitems as (select * from production.orderitems);

CREATE OR REPLACE view analysis.view_orders as (select * from production.orders); 

CREATE OR REPLACE view analysis.view_orderstatuses as (select * from production.orderstatuses); 

CREATE OR REPLACE view analysis.view_orderstatuslog as (select * from production.orderstatuslog); 

CREATE OR REPLACE view analysis.view_products as (select * from production.products); 

CREATE OR REPLACE view analysis.view_users as (select * from production.users); 
