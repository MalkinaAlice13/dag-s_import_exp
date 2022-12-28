insert into analysis.tmp_rfm_frequency (user_id, frequency)
with 
users as (
	select distinct user_id from analysis.view_orders),
users_and_order_ts as (
	select  
		user_id,
		count(status) count_orders 
	FROM analysis.view_orders
	where status = 4
	group by 1),
over_count_ord as (
	select 
		u.user_id,
		count_orders,
		row_number () over(order by count_orders) over_count_orders
	from users u left join users_and_order_ts u_t
	on u.user_id = u_t.user_id),
itog as (
	select *,
	case 
		when count_orders is null then 1
		when over_count_orders between 1 and 188 then 1
		when over_count_orders between 189 and 388 then 2
		when over_count_orders between 389 and 588 then 3
		when over_count_orders between 589 and 788 then 4
		else 5 end frequency 
	from over_count_ord)

select user_id, frequency from itog