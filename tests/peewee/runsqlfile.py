import unittest
from src.models import db
from src.log import logger

class TestProject(unittest.TestCase):
    def peewee_exec_raw_sql(self):
        """
        python -m unittest tests.TestProject.peewee_exec_raw_sql
        """
        # cursor = db.cursor()
        sql=None
        sqlpath=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\assets\country-db\world_area-sqlite.sql'
        with open(sqlpath,encoding='utf-8') as f:
            sql=f.read()
        with db:
            print(sql)
        #     sql = """
        #     SELECT 
        #         `account`.`id`,
        #         `account`.`name`,
        #         `order`.`product_id`
        #     FROM 
        #         `account`
        #         INNER JOIN `order` ON (`account`.`id` = `order`.`user_id`)
        #     """
            db.execute(sql)
            db.connection.commit() # 这里必须要提交，不然所有的查询都会处于一个事务中
            rows: tuple[tuple] = db.fetchall()

            for row in rows:
                logger.debug(row)
t=TestProject()
t.peewee_exec_raw_sql()
