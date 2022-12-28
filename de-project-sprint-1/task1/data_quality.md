# 1.3. Качество данных

## Оцените, насколько качественные данные хранятся в источнике.
Опишите, как вы проверяли исходные данные и какие выводы сделали.

## Укажите, какие инструменты обеспечивают качество данных в источнике.
Ответ запишите в формате таблицы со следующими столбцами:
- `Наименование таблицы` - наименование таблицы, объект которой рассматриваете.
- `Объект` - Здесь укажите название объекта в таблице, на который применён инструмент. Например, здесь стоит перечислить поля таблицы, индексы и т.д.
- `Инструмент` - тип инструмента: первичный ключ, ограничение или что-то ещё.
- `Для чего используется` - здесь в свободной форме опишите, что инструмент делает.

Пример ответа:

production.(...)

| Таблицы  | Объект                                  | Инструмент      | Для чего используется                             |
| -------- | --------------------------------------- | --------------- | --------------------------------------------------|
| users    | id int4 NOT NULL PRIMARY KEY            | Первичный ключ  | Обеспечивает уникальность записей                 |
| users    | name varchar(2048) NULL                 | Опция NULL      | Допускает пустое значение в строке                |
| users    | login varchar(2048) NOT NULL            | Опция NOT NULL  | Не допускает пустое значение в строке             |
| Products | id int4 NOT NULL PRIMARY KEY            | Первичный ключ  | Обеспечивает уникальность записей                 |
| Products | name varchar(2048) NOT NULL             | Опция NULL      | Допускает пустое значение в строке                |
| Products | price numeric(19, 5) NOT NULL DEFAULT 0 | DEFAULT 0       | Принимает зн. 0, если другое значение не указано  |
| orderitems | id int4 NOT NULL GENERATED ALWAYS AS IDENTITY | GENERATED      | Автомат. присваивает столбцу уникальный номер    |
| orderitems | product_id int4 NOT NULL                      | Внешний ключ   | Обеспечивает связь таблиц                        |
| orderitems | order_id int4 NOT NULL                        | Внешний ключ   | Обеспечивает связь таблиц                        |
| orderitems | name varchar(2048) NOT NULL                   | Опция NOT NULL | Не допускает пустое значение в строке            |
| orderitems | price numeric(19, 5) NOT NULL DEFAULT 0       | DEFAULT 0      | Принимает зн. 0, если другое значение не указано |
| orderitems | discount numeric(19, 5) NOT NULL DEFAULT 0    | DEFAULT 0      | Принимает зн. 0, если другое значение не указано |
| orderitems | quantity int4 NOT NULL                        | Опция NOT NULL | Не допускает пустое значение в строке            |
| orders | order_id int4 NOT NULL                          | Внешний ключ   | Обеспечивает связь таблиц                        |
| orders | order_ts timestamp NOT NULL                     | Опция NOT NULL | Не допускает пустое значение в строке            |
| orders | user_id int4 NOT NULL                           | Внешний ключ   | Обеспечивает связь таблиц                        |
| orders | bonus_payment numeric(19, 5) NOT NULL DEFAULT 0 | DEFAULT 0      | Не допускает пустое значение в строке            |
| orders | payment numeric(19, 5) NOT NULL DEFAULT 0       | DEFAULT 0      | Принимает зн. 0, если другое значение не указано |
| orders | "cost" numeric(19, 5) NOT NULL DEFAULT 0        | DEFAULT 0      | Принимает зн. 0, если другое значение не указано |
| orders | bonus_grant numeric(19, 5) NOT NULL DEFAULT 0   | DEFAULT 0      | Принимает зн. 0, если другое значение не указано |
| orders | status int4 NOT NULL                            | Опция NOT NULL | Не допускает пустое значение в строке            |
| orderstatuslog | id int4 NOT NULL GENERATED ALWAYS AS IDENTITY | GENERATED      | Автомат. присваивает столбцу уникальный номер |
| orderstatuslog | order_id int4 NOT NULL                        | Внешний ключ   | Обеспечивает связь таблиц                     |
| orderstatuslog | status_id int4 NOT NULL                       | Внешний ключ   | Обеспечивает связь таблиц                     |
| orderstatuslog | dttm timestamp NOT NULL                       | Опция NOT NULL | Не допускает пустое значение в строке         |
| orderstatuses | id int4 NOT NULL          | Первичный ключ | Обеспечивает уникальность записей     |
| orderstatuses | key varchar(255) NOT NULL | Опция NOT NULL | Не допускает пустое значение в строке |
