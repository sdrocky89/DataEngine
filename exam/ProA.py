import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
html = requests.get(url)
html_page = html.text
soup = BeautifulSoup(html_page,'html.parser')

carinfo = soup.find('div',class_="search-result-list")
df = pd.DataFrame(columns=['car_model','low_price','high_price','photo'])
list = carinfo.find_all('div',class_='search-result-list-item')

for div in list:
    temp={}
    #取车型名称
    name = div.find('p',class_='cx-name text-hover').text
    #取价格，如果结果为暂无，则最低价，最高价皆为暂无，否则以‘-’符号进行分隔
    price = div.find('p',class_='cx-price').text
    if price == '暂无':
        low_price = '暂无'
        high_price = '暂无'
    else:
        low_price = re.split('-',price)[0]+'万'
        high_price = re.split('-',price)[1]
    #取图片地址
    img_ = div.find(name='img').get('src')
    #装入df中
    temp['car_model'],temp['low_price'],temp['high_price'],temp['photo'] = name,low_price,high_price,img_
    df = df.append(temp,ignore_index = True)
    #print(price,low_price,high_price)
#print(df)
df.to_csv('./result.csv',index = False,encoding='utf_8_sig')
