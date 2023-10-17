import json
from logging import Logger
from datetime import datetime
from typing import List, Optional

from psycopg.rows import class_row
from pydantic import BaseModel
from lib import PgConnect
from lib.dict_util import json2str

from examples.dds.dds_settings_repository import DdsEtlSettingsRepository, EtlSetting

from examples.dds.dm_products_dag.dm_products_loader import (ProductDdsObj, ProductDdsRepository)
from examples.dds.dm_orders_dag.dm_orders_loader import (OrderDdsObj,OrderJsonObj,OrderRawRepository,OrderDdsRepository)


class SalesDdsObj(BaseModel):
    id: int
    product_id: int #FK на dm_products.id
    order_id: int #FK на dm_orders.id
    count: int #stg.bonussystem_events.product_payments.quantity
    price: float #stg.bonussystem_events.product_payments.price
    total_sum: float #цена * количество (quantity*price)
    bonus_payment: float #stg.bonussystem_events.product_payments.bonus_payment
    bonus_grant: float #stg.bonussystem_events.product_payments.bonus_grant


class SalesJsonObj(BaseModel):
    id: int
    event_ts: datetime
    event_type: str
    event_value: str


class ProductPayments(BaseModel): #для подгрузки каждой строки
    product_id: str
    product_name: str
    price: int
    quantity: int
    product_cost: int
    bonus_payment: float
    bonus_grant: int


class SalesRawRepository:
    def load_raw_sales(self, conn: PgConnect, last_loaded_record_id: int) -> List[SalesJsonObj]:
        with conn.cursor(row_factory=class_row(SalesJsonObj)) as cur:
            cur.execute(
                """
                    SELECT 
                    id, 
                    event_ts, 
                    event_type, 
                    event_value
                    FROM stg.bonussystem_events
                    --WHERE id > %(last_loaded_record_id)s
                    ORDER BY id ASC;
                """,
                {"last_loaded_record_id": last_loaded_record_id},
            )
            objs = cur.fetchall()
        objs.sort(key=lambda x: x.id)
        return objs


class SalesDdsRepository:
    def insert_sales(self, conn: PgConnect, sales: List[ProductPayments]) -> None: #List[ProductDdsObj] ##List[SalesDdsObj]
        with conn.cursor() as cur:
            #for sale in sales:
            cur.execute(
                """
                    INSERT INTO dds.fct_product_sales (product_id, order_id, count, price, total_sum, bonus_payment, bonus_grant)
                    VALUES (%(product_id)s, %(order_id)s, %(count)s, %(price)s, %(total_sum)s, %(bonus_payment)s, %(bonus_grant)s);
                """,
                {
                    "product_id": sales.product_id,
                    "order_id": sales.order_id,
                    "count": sales.count,
                    "price": sales.price,
                    "total_sum": sales.total_sum,
                    "bonus_payment": sales.bonus_payment,
                    "bonus_grant": sales.bonus_grant
                },
            )
            conn.commit()

    def get_sales(self, conn: PgConnect, id: int) -> Optional[OrderDdsObj]:
        with conn.cursor(row_factory=class_row(OrderDdsObj)) as cur:
            cur.execute(
                """
                    SELECT 
                    id, 
                    product_id, 
                    order_id, 
                    count, 
                    price, 
                    total_sum, 
                    bonus_payment, 
                    bonus_grant
                    FROM dds.fct_product_sales
                    WHERE order_key = %(order_key)s;
                """,
                {"id": id},
            )
            obj = cur.fetchone()
            conn.commit()
        return obj



class SalesLoader:
    WF_KEY = "sales_raw_to_dds_workflow"
    LAST_LOADED_ID_KEY = "last_loaded_id"

    def __init__(self, conn: PgConnect, log: Logger) -> None:
        self.dwh = conn
        self.settings_repository = DdsEtlSettingsRepository()
        self.log = log
        self.raw = SalesRawRepository()
        self.dds_sales = SalesDdsRepository()
        self.dds_products = ProductDdsRepository()
        self.dds_orders = OrderDdsRepository()

    def parse_sales(self, raws: List[ProductPayments], product_id: int, order_id: int) -> List[SalesDdsObj]: #: List[SalesJsonObj]
        #res = []
        #sales_json = json.loads(raws)
        #print(sales_json)
        t = SalesDdsObj(
                            id=0,
                            product_id=product_id,
                            order_id=order_id,
                            count=raws['quantity'],
                            price=raws['price'],
                            total_sum=raws['product_cost'],
                            bonus_payment=raws['bonus_payment'],
                            bonus_grant=raws['bonus_grant']
                                            )
            #res.append(t)
        print('parse_sales: ', t)
        return t
    """
    def parse_order_products(self,
                             order_raw: BonusPaymentJsonObj,
                             order_id: int,
                             products: Dict[str, ProductDdsObj]
                             ) -> Tuple[bool, List[FctProductDdsObj]]:

        res = []

        for p_json in order_raw.product_payments:
            if p_json.product_id not in products:
                return (False, [])

            t = FctProductDdsObj(id=0,
                                 order_id=order_id,
                                 product_id=products[p_json.product_id].id,
                                 count=p_json.quantity,
                                 price=p_json.price,
                                 total_sum=p_json.product_cost,
                                 bonus_grant=p_json.bonus_grant,
                                 bonus_payment=p_json.bonus_payment
                                 )
            res.append(t)
        return res
    """
    def dm_load_sales(self):
        with self.dwh.connection() as conn:
            wf_setting = self.settings_repository.get_setting(conn, self.WF_KEY)
            if not wf_setting:
                wf_setting = EtlSetting(id=0, workflow_key=self.WF_KEY, workflow_settings={self.LAST_LOADED_ID_KEY: -1})

            last_loaded_id = wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY]

            load_queue = self.raw.load_raw_sales(conn, last_loaded_id)
            load_queue.sort(key=lambda x: x.id) # хотела брать каждую третью запись: % 3 != 0

            for sales_raw in load_queue:
                sales_json = json.loads(sales_raw.event_value)

                if 'product_payments' in sales_json:
                    for p_id in range(len(sales_json['product_payments'])):
                        product = self.dds_products.get_product(conn, sales_json['product_payments'][p_id]['product_id'])
                        product_p_id_info = sales_json['product_payments'][p_id]
                        if not product:
                            break

                        order = self.dds_orders.get_order(conn, sales_json['order_id'])
                        if not order:
                            break

                        print('product.id: ', product.id, 'order.id: ', order.id) # 39 24
                        print('sales_raw: ', sales_raw)
                        print(sales_json['product_payments'][p_id]['product_id'])
                        print(sales_json['product_payments'][p_id])

                        #sales_to_load = self.parse_sales(sales_raw, product.id, order.id)
                        sales_to_load = self.parse_sales(product_p_id_info, product.id, order.id)

                        self.dds_sales.insert_sales(conn, sales_to_load)

                        wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY] = sales_raw.id
                        #max(sales_raw.id, wf_setting.workflow_settings[self.LAST_LOADED_ID_KEY])
                        wf_setting_json = json2str(wf_setting.workflow_settings)
                        self.settings_repository.save_setting(conn, wf_setting.workflow_key, wf_setting_json)
                else:
                    continue




