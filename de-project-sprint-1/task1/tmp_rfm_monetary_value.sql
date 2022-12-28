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
	group by 1),
over_sum_ord as (
	select 
		u.user_id,
		cost_,
		row_number () over(order by cost_) over_sum_orders
	from users u left join users_and_order_ts u_t
	on u.user_id = u_t.user_id),
itog as (
	select *,
	case 
		when cost_ is null then 1
		when over_sum_orders between 1 and 188 then 1
		when over_sum_orders between 189 and 388 then 2
		when over_sum_orders between 389 and 588 then 3
		when over_sum_orders between 589 and 788 then 4
		else 5 end monetary_value
	from over_sum_ord)
		
select user_id, monetary_value from itog