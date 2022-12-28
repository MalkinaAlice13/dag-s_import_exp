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