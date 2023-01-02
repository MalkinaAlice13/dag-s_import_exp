insert into analysis.tmp_rfm_recency (user_id, recency)
with 
users as (
	select distinct user_id from analysis.view_orders),
users_and_order_ts as (
	select  
		user_id,
		max(order_ts) order_ts
	FROM analysis.view_orders
	where status = 4 and extract(year from order_ts) = 2022
	group by 1)
select 
	u.user_id, 
	ntile (5) over(order by u_t.order_ts NULLS FIRST) recency
from users u 
left join users_and_order_ts u_t 
on u.user_id = u_t.user_id
