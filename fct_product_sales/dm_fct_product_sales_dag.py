import logging
import pendulum
from airflow.decorators import dag, task
from examples.dds.dm_fct_product_sales.dm_fct_product_sales_loader import SalesLoader
from lib import ConnectionBuilder

log = logging.getLogger(__name__)

@dag(
    schedule_interval='0/5 * * * *',  # Задаем расписание выполнения дага - каждый 15 минут.
    start_date=pendulum.datetime(2023, 9, 2, tz="UTC"),  # Дата начала выполнения дага. Можно поставить сегодня.
    catchup=False,  # Нужно ли запускать даг за предыдущие периоды (с start_date до сегодня) - False (не нужно).
    tags=['sprint5', 'dds', 'origin', 'example'],  # Теги, используются для фильтрации в интерфейсе Airflow.
    is_paused_upon_creation=True  # Остановлен/запущен при появлении. Сразу запущен.
)
def sprint5_example_dds_dm_fct_product_sales_dag():
    # Создаем подключение к базе dwh.
    dwh_pg_connect = ConnectionBuilder.pg_conn("PG_WAREHOUSE_CONNECTION")

    # Создаем подключение к базе подсистемы бонусов.
    #origin_pg_connect = ConnectionBuilder.pg_conn("PG_WAREHOUSE_CONNECTION")

    # Объявляем таск, который загружает данные.
    @task(task_id="dm_load_sales")
    def dm_load_sales():
        # создаем экземпляр класса, в котором реализована логика.
        rest_loader = SalesLoader(dwh_pg_connect, log) #origin_pg_connect
        rest_loader.dm_load_sales()  # Вызываем функцию, которая перельет данные.

    # Инициализируем объявленные таски.
    dm_sales_dict = dm_load_sales()

    # Далее задаем последовательность выполнения тасков.
    # Т.к. таск один, просто обозначим его здесь.
    dm_sales_dict  # type: ignore


dds_dm_sales_dag = sprint5_example_dds_dm_fct_product_sales_dag()
