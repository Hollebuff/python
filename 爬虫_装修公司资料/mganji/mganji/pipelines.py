# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class MganjiPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='localhost', user='root', password='root', database='db_company', charset='utf8')
        cur = conn.cursor()
        sql = "INSERT INTO tb_mganji(id, company_url, city_name, company_add, company_name, linkman, tel)" \
              "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        parmitem = (item['id'], item['company_url'], item['city_name'], item['company_add'],
                    item['company_name'], item['linkman'], item['tel'])
        try:
            cur.execute(sql, parmitem)
        except Exception:
            conn.rollback()
        else:
            conn.commit()
        cur.close()
        conn.close()
        return item
