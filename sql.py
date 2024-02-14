import json
import sqlite3
import requests

#定义函数
def get_location(x):
    # 构建请求 
    key = "75f3c8650855fe5372f3fe79761265df"
    url = f'https://restapi.amap.com/v3/geocode/geo?address={x}&output=JSON&key={key}'
    # 发送请求
    response = requests.get(url)
    # 打印结果
    print(response.text)
    # 解析数据
    json_data = json.loads(response.text)
    # 获取信息
    geo = json_data["geocodes"][0]["location"]
    # geo_d = json_data["geocodes"][0]["formatted_address"]
    return geo

conn = sqlite3.connect('address.db')
cur = conn.cursor()
cur.execute("CREATE TABLE address(line_location TEXT,location TEXT);")

with open("address.txt","r",encoding='utf-8') as f:
    for line in f.readlines():
        line_location = line.strip() # 去除可能的空格和换行符
        location = get_location(line)
        #创建list
        data = [line_location,location]
        # 写入数据
        cur.execute("INSERT INTO address VALUES (?,?)",data)

conn.commit() #对数据库做改动后（比如建表、插数等），都需要手动提交改动，否则无法将数据保存到数据库。
# 关闭游标
cur.close()
# 关闭连接
conn.close()
