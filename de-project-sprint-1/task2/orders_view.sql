CREATE OR REPLACE VIEW analysis.view_orders AS 

with 
status as (
	select order_id, status_id from (
select *,
row_number () over (partition by order_id order by dttm desc) over_
from production.orderstatuslog
	) tabl_over where over_ = 1)

select DISTINCT
	o.order_id,
	o.order_ts,
	o.user_id,
	o.bonus_payment,
	o.payment,
	o."cost",
	o.bonus_grant,
	s.status_id as status 
from production.orders o
join status s on o.order_id = s.order_id

----НО МОЖНО И ТАК----

SELECT 
    DISTINCT o.order_id,
    o.order_ts,
    o.user_id,
    o.bonus_payment,
    o.payment,
    o."cost",
    o.bonus_grant,
    LAST_VALUE(p.status_id) OVER (PARTITION BY p.order_id ORDER BY dttm ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS status
FROM 
    production.orders AS o
JOIN
    production.orderstatuslog AS p
        USING(order_id) 
