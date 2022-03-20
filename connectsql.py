import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='TESTDB')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 音频路径
path = "G:\Words_Hearing\Speech_US\\2022-03-08"

pymysql.Binary()

#
# # SQL 创表
# sql = """CREATE TABLE EMPLOYEE(
#           WORDS_NAME,CHAR(20),
#           DATA VARBINARY(10240))"""
#
# cursor.execute(sql)

# 关闭数据库连接
db.close()