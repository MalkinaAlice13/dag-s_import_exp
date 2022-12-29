CREATE OR REPLACE VIEW analysis.view_orders AS 

with 
order_dttm as (
    select
        order_id ,
        max(dttm) dttm 
    from production.orderstatuslog 
    group by 1),
itog as (
        select od.*, 
        vo.status_id as status
    from order_dttm od
    left join production.orderstatuslog vo 
    on od.order_id = vo.order_id and od.dttm = vo.dttm),
old_orders as (
    select 
        order_id,
        order_ts,
        user_id,
        bonus_payment,
        payment,
        "cost",
        bonus_grant
    from production.orders)

select 
    o.*,
    i.status
from old_orders o 
join itog i on o.order_id = i.order_id
