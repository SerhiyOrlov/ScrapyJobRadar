from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from items import Vacancy
import psycopg2
import redis
import logging


class RedisIsUniquePipeline:
    def __init__(self, redis_url):
        self.redis_url = redis_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_url=crawler.settings.get("REDIS_URL"),
        )

    def open_spider(self, spider):
        self.r = redis.from_url(self.redis_url)

    def close_spider(self):
        self.r.close()

    def process_item(self, item: Vacancy, spider):
        adapter = ItemAdapter(item)
        is_new = self.r.sadd('vacancy_unique', adapter["external_id"])
        if not is_new:
            logging.info(f'Found dublicate: {adapter["external_id"]}')
            raise DropItem(f"Duplicate: {adapter['external_id']}")


class PostgesSQLWriter:
    def __init__(self):
        self.connection = psycopg2.connect(
                                database='jobradar',
                                user='jobradar',
                                password=self.postgress_pass,
                                host=self.database_url,
                                port=5432
                                        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            postgress_pass=crawler.settings.get("POSTGRES_PASSWORD"),
            database_url=crawler.settings.get("DATABASE_URL")
        )

    def open_spider(self, item, spyder):
        cursor = self.connection.cursor()

# TODO: Add Logging
