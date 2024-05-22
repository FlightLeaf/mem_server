import psycopg2
from psycopg2 import pool

# 创建连接池
pg_pool = psycopg2.pool.SimpleConnectionPool(
    1,  # 最小连接数
    50,  # 最大连接数
    host="139.196.89.94",
    port="5433",
    database="db3cc04a6054804552adb6870d9d428ddcmem_520am",
    user="root_am",
    password="Lvbaochun1228",
    options="-c timezone=Asia/Shanghai"
)

if pg_pool is None:
    print("连接池创建失败")
    exit(1)
else:
    print("连接池创建成功")


def get_connection():
    """获取数据库连接"""
    return pg_pool.getconn()


def release_connection(connection):
    """释放数据库连接"""
    pg_pool.putconn(connection)


def close_all():
    """关闭所有连接并清理资源"""
    pg_pool.closeall()
