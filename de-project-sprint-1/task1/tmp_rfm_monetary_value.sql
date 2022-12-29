insert into analysis.tmp_rfm_monetary_value (user_id, monetary_value)
with 
users as (
	select distinct user_id from analysis.view_orders),
users_and_order_ts as (
	select  
		user_id,
		sum("cost") as cost_
	FROM analysis.view_orders
	where status = 4
	group by 1)

select 
	u.user_id,
	NTILE(5) OVER(ORDER by coalesce(cost_, 0)) monetary_value
from users u left join users_and_order_ts u_t
on u.user_id = u_t.user_id
