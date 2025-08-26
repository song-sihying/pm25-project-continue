import pymysql
import requests

table_str="""
create table if not exists pm25(
id int auto_increment primary key,
site varchar(25),
county varchar(50),
pm25 int,
datacreationdate datetime,
itemunit varchar(20),
unique key site_time (site,datacreationdate)
)
"""

sqlstr="insert ignore into pm25(site,county,pm25,datacreationdate,itemunit)\
      values(%s,%s,%s,%s,%s)"

url="https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=JSON"

conn,cursor=None,None

def open_db():
    global conn,cursor
    
    try:
        conn=pymysql.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="demo"
        )
        
        #print(conn)  
        cursor=conn.cursor()  
        print("資料庫開啟成功!")
    except Exception as e:
        print(e)

def close_db():
    if conn is not None:
        conn.close()
        print("資料庫關閉成功!")


def get_open_data():
    resp=requests.get(url,verify=False)
    datas=resp.json()['records']
    values=[list(data.values()) for data in datas if list(data.values())[2]!=""]
    return values

def write_to_sql():
    try:
        values=get_open_data()
        if len(values)==0:
            print("目前無資料")
            return

        size=cursor.executemany(sqlstr,values)
        conn.commit()    
        print(f"寫入{size}筆資料成功!")
    except Exception as e:
        print(e)


#open_db()
#write_to_sql()
#close_db()
