insert into analysis.tmp_rfm_recency (user_id, recency)
with 
users as (
	select distinct user_id from analysis.view_orders),
users_and_order_ts as (
	select  
		user_id,
		max(order_ts) order_ts
	FROM analysis.view_orders
	where status = 4
	group by 1),
num_order_ts as (
	select 
		u.user_id, 
		u_t.order_ts,
		row_number () over (order by u_t.order_ts) num
	from users u 
	left join users_and_order_ts u_t 
	on u.user_id = u_t.user_id),
itog as (
	select *,
	case 
		when order_ts is null then 1
		when num between 1 and 188 then 1
		when num between 189 and 388 then 2
		when num between 389 and 588 then 3
		when num between 589 and 788 then 4
		else '5' end recency 
	from num_order_ts)

select user_id, recency from itog