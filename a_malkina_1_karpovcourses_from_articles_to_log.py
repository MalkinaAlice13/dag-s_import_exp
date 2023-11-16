"""
Работать с понедельника по субботу, но не по воскресеньям
Используйте соединение 'conn_greenplum'
Забирать из таблицы articles значение поля heading из строки с id, равным дню недели ds (понедельник=1, вторник=2, ...)
Выводить результат работы в любом виде: в логах либо в XCom'е
Даты работы дага: с 1 марта 2022 года по 14 марта 2022 года
"""

from airflow import DAG
import pendulum
import logging
import jinja2
from airflow.hooks.postgres_hook import PostgresHook  # c помощью этого hook будем входить в наш Greenplum
from airflow.operators.python_operator import PythonOperator

DEFAULT_ARGS = {
    'start_date': pendulum.datetime(2022, 3, 1, tz="UTC"),
    'end_date': pendulum.datetime(2022, 3, 14, tz="UTC"),
    'owner': 'a-malkina-1',
    'poke_interval': 600
    # это время в секундах, в течение которого датчик ожидает, прежде чем снова проверить условие
}

with DAG("a_malkina_1_from_articles_to_log",
         schedule_interval='0 0 * * 1-6',  # Задаем расписание выполнения дага - с пн по сб (0/7 вс)
         default_args=DEFAULT_ARGS,
         max_active_runs=1,
         tags=['a-malkina-1']
         ) as dag:

        dt = '{{ ds }}'

        def get_articles(dt):
            pg_hook = PostgresHook(postgres_conn_id='conn_greenplum')  # инициализируем хук
            conn = pg_hook.get_conn()  # берём из него соединение
            cursor = conn.cursor("named_cursor_name")
            cursor.execute(f"""SELECT heading FROM articles WHERE id = date_part('isodow','{dt}'::date)""""")
            one_string = cursor.fetchone()[0]  # если вернулось единственное значение
            logging.info(one_string)


        get_articles_func = PythonOperator(
            task_id='get_articles_task',
            python_callable=get_articles,
            op_kwargs={'dt': dt}
        )

        get_articles_func
