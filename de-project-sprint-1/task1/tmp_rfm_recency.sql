insert into analysis.tmp_rfm_recency (user_id, recency)
with 
users as (
	select distinct user_id from analysis.view_orders ),
users_and_order_ts as (
	select  
		user_id,
		max(order_ts) order_ts
	FROM analysis.view_orders
	where status = 4
	group by 1)

select 
	u.user_id, 
	NTILE(5) OVER(ORDER by coalesce (u_t.order_ts, (select min(order_ts) from users_and_order_ts))) recency
from users u 
left join users_and_order_ts u_t 
on u.user_id = u_t.user_id
