insert into analysis.tmp_rfm_frequency (user_id, frequency)
with 
users as (
	select distinct user_id from analysis.view_orders),
count_status as (
	select  
		user_id,
		count(status) count_orders 
	FROM analysis.view_orders
	where status = 4 and extract(year from order_ts) = 2022
	group by 1)

select 
	u.user_id,
	NTILE(5) OVER(ORDER by coalesce(u_t.count_orders, 0)) frequency
from users u left join count_status u_t
on u.user_id = u_t.user_id
