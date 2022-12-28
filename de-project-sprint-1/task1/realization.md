# Витрина RFM

## 1.1. Выясните требования к целевой витрине.

Постановка задачи выглядит достаточно абстрактно - постройте витрину. Первым делом вам необходимо выяснить у заказчика детали. Запросите недостающую информацию у заказчика в чате.

Зафиксируйте выясненные требования. Составьте документацию готовящейся витрины на основе заданных вами вопросов, добавив все необходимые детали.

-----------
RFM (от англ. Recency, Frequency, Monetary Value) — способ сегментации клиентов, при котором анализируют их лояльность: как часто, на какие суммы и когда в последний раз тот или иной клиент покупал что-то. На основе этого выбирают клиентские категории, на которые стоит направить маркетинговые усилия. 

## Каждого клиента оценивают по трём факторам:

Recency (пер. «давность») — сколько времени прошло с момента последнего заказа.

Frequency (пер. «частота») — количество заказов.

Monetary Value (пер. «денежная ценность») — сумма затрат клиента.

## Как провести RFM-сегментацию
Присвойте каждому клиенту три значения — значение фактора Recency, значение фактора Frequency и значение фактора Monetary Value:
 
Фактор Recency измеряется по последнему заказу. Распределите клиентов по шкале от одного до пяти, где значение 1 получат те, кто либо вообще не делал заказов, либо делал их очень давно, а 5 — те, кто заказывал относительно недавно.

Фактор Frequency оценивается по количеству заказов. Распределите клиентов по шкале от одного до пяти, где значение 1 получат клиенты с наименьшим количеством заказов, а 5 — с наибольшим.

Фактор Monetary Value оценивается по потраченной сумме. Распределите клиентов по шкале от одного до пяти, где значение 1 получат клиенты с наименьшей суммой, а 5 — с наибольшей.

Проверьте, что количество клиентов в каждом сегменте одинаково. Например, если в базе всего 100 клиентов, то 20 клиентов должны получить значение 1, ещё 20 — значение 2 и т. д.

## Необходимые детали:

1. Витрина должна располагаться в той же базе в схеме analysis.
2. Витрина должна состоять из таких полей:

    - user_id,

    - recency (число от 1 до 5),

    - frequency (число от 1 до 5),

    - monetary_value (число от 1 до 5).

3. В витрине нужны данные с начала 2022 года.
4. Назовите витрину dm_rfm_segments.
5. Обновления не нужны. 
6. Успешно выполненный заказ - заказ со статусом Closed.

## Доступы и базы данных

Вам дали доступ к базе данных компании. В базе две схемы: production и analysis. В схеме production содержатся оперативные таблицы.
Задача — построить витрину для RFM-классификации. Для анализа нужно отобрать только успешно выполненные заказы.

## 1.2. Изучите структуру исходных данных.

Подключитесь к базе данных и изучите структуру таблиц.

Если появились вопросы по устройству источника, задайте их в чате.

Зафиксируйте, какие поля вы будете использовать для расчета витрины.

-----------

### production.users:
   - id - идентификатор пользователя;
   - name - никнейм;
   - login - ФИО клиента.

### production.products (меню):
   - id - идентификатор продукта;
   - name - название продукта;
   - price - цена продукта.

### production.orderstatuslog (журнал статусов заказа):
   - id - уникальный идентификатор строки;
   - order_id - идентификатор заказа;
   - status_id - статус заказа;
   - dttm - дата/время изменения статуса заказа.

### production.orderstatuses:
   - id - идентификатор статуса заказа;
   - key - статус (имя) заказа (значения: Open, Cooking, Delivering, Closed, Cancelled).

### production.orders (о заказе):
   - order_id - идентификатор заказа;
   - order_ts - дата и время заказа (timestamp);
   - user_id - идентификатор пользователя;
   - bonus_payment - бонус-платеж;
   - payment - сумма оплаты;
   - cost - стоимость заказа;
   - bonus_grant - бонус-грант;
   - status - идентификатор статуса заказа (5 - Cancelled - Отменен; 4 - Closed - Закрыт (успешный)).

### production.orderitems (заказ продуктов):
   - id - уникальный идентификатор строки;
   - product_id - идентификатор продукта;
   - order_id - идентификатор заказа;
   - name - название продукта;
   - price - цена продукта;
   - discount - скидка на заказ;
   - quantity - количество этого товара.

## Используемые поля для подсчета факторов:

1. RECENCY (количество времени, прошедшего с последнего успешно выполненного заказа):
   
    - production.orders.order_ts (дата и время заказа (2022 год))

    - production.orders.status ( = 4 )

    - production.orders.user_id (идентификатор клиента)

2. FREQUENCY (количество успешных заказов клиента)
   
    - production.orders.status ( = 4 )

    - production.orders.user_id (идентификатор клиента)

    - production.orders.order_ts (дата и время заказа (2022 год))

3. MONEYTARY VALUE (сумма затрат клиента на успешные заказы):

    - production.orders.cost (стоимость заказа)

    - production.orders.status ( = 4 )

    - production.orders.user_id (идентификатор клиента)

    - production.orders.order_ts (дата и время заказа (2022 год))

## 1.3. Проанализируйте качество данных

Изучите качество входных данных. Опишите, насколько качественные данные хранятся в источнике. Так же укажите, какие инструменты обеспечения качества данных были использованы в таблицах в схеме production.

-----------
### production.orderitems (NOT NULL | NOT NULL DEFAULT 0)
```SQL
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	product_id int4 NOT NULL,
	order_id int4 NOT NULL,
	"name" varchar(2048) NOT NULL,
	price numeric(19, 5) NOT NULL DEFAULT 0,
	discount numeric(19, 5) NOT NULL DEFAULT 0,
	quantity int4 NOT NULL
```
### production.orders (NOT NULL | NOT NULL DEFAULT 0)
```SQL
	order_id int4 NOT NULL,
	order_ts timestamp NOT NULL,
	user_id int4 NOT NULL,
	bonus_payment numeric(19, 5) NOT NULL DEFAULT 0,
	payment numeric(19, 5) NOT NULL DEFAULT 0,
	"cost" numeric(19, 5) NOT NULL DEFAULT 0,
	bonus_grant numeric(19, 5) NOT NULL DEFAULT 0,
	status int4 NOT NULL
```
### production.orderstatuses (NOT NULL)
```SQL
	id int4 NOT NULL,
	"key" varchar(255) NOT NULL
```
### production.orderstatuslog (NOT NULL)
```SQL
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	order_id int4 NOT NULL,
	status_id int4 NOT NULL,
	dttm timestamp NOT NULL
```
### production.products (NOT NULL)
```SQL
	id int4 NOT NULL,
	"name" varchar(2048) NOT NULL,
	price numeric(19, 5) NOT NULL DEFAULT 0
```
### production.users (NOT NULL | PRIMARY KEY)
```SQL
	id int4 NOT NULL,
	"name" varchar(2048) NULL,
	login varchar(2048) NOT NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id)
```

## 1.4. Подготовьте витрину данных

Теперь, когда требования понятны, а исходные данные изучены, можно приступить к реализации.

### 1.4.1. Сделайте VIEW для таблиц из базы production.**

Вас просят при расчете витрины обращаться только к объектам из схемы analysis. Чтобы не дублировать данные (данные находятся в этой же базе), вы решаете сделать view. Таким образом, View будут находиться в схеме analysis и вычитывать данные из схемы production. 

Напишите SQL-запросы для создания пяти VIEW (по одному на каждую таблицу) и выполните их. Для проверки предоставьте код создания VIEW.

```SQL
create view analysis.view_orderitems as (select * from production.orderitems);

create view analysis.view_orders as (select * from production.orders); 

create view analysis.view_orderstatuses as (select * from production.orderstatuses); 

create view analysis.view_orderstatuslog as (select * from production.orderstatuslog); 

create view analysis.view_products as (select * from production.products); 

create view analysis.view_users as (select * from production.users); 
```

### 1.4.2. Напишите DDL-запрос для создания витрины.**

Далее вам необходимо создать витрину. Напишите CREATE TABLE запрос и выполните его на предоставленной базе данных в схеме analysis.

```SQL
create table analysis.tmp_rfm_recency (
user_id int not null primary key,
recency int not null check (recency >= 1 and recency <= 5));

create table analysis.tmp_rfm_frequency (
user_id int not null primary key,
frequency int not null check (frequency >= 1 and frequency <= 5));

create table analysis.tmp_rfm_monetary_value (
user_id int not null primary key,
monetary_value int not null check (monetary_value >= 1 and monetary_value <= 5));

create table analysis.dm_rfm_segments (
user_id int not null primary key,
recency int,
frequency int,
monetary_value int);
```

### 1.4.3. Напишите SQL запрос для заполнения витрины

Наконец, реализуйте расчет витрины на языке SQL и заполните таблицу, созданную в предыдущем пункте.

Для решения предоставьте код запроса.

```SQL
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
```
```SQL
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
```
```SQL
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
```
```SQL
insert into analysis.dm_rfm_segments (user_id,recency,frequency,monetary_value)
select 
m.user_id,
r.recency,
f.frequency,
m.monetary_value
from 
analysis.tmp_rfm_monetary_value m 
join analysis.tmp_rfm_recency r on m.user_id  = r.user_id 
join analysis.tmp_rfm_frequency f on m.user_id = f.user_id 
```


