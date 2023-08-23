# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.sql import null
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from av_parse.models import PriceItem, db_connect, create_table

class AvParsePipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        priceitem = PriceItem()
        priceitem.good_name = item["good_name"]
        priceitem.price = float(item["price"])
        priceitem.price_old = float(item["price_old"]) if item["price_old"] else null()
        priceitem.img_url = item["img_url"]
        priceitem.url = item["url"]
        priceitem.unit_raw = item["unit_raw"]
        priceitem.item_id = item["item_id"]
        priceitem.category = item["category"]
        priceitem.region = item["region"]
        priceitem.retailer_name = item["retailer_name"]

        try:
            session.add(priceitem)
            session.commit()
            session.refresh(priceitem)
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
