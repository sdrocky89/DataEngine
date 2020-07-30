import pandas as pd
from efficient_apriori import apriori as apr

data = pd.read_csv('./订单表.csv',encoding='gbk')
data = data.sort_values(by='客户ID',ascending = True)
#print(data.head())

orders_series = data.set_index('客户ID')['产品型号名称']

#将相同客户ID的产品型号名称合并在同一条，将所有信息放入测试集
transactions = []
temp_index = 0
for i, v in orders_series.items():
    if i != temp_index:
        temp_set = set()
        temp_index = i
        temp_set.add(v)
        transactions.append(temp_set)
    else:
        temp_set.add(v)
print(transactions)
#调用apriori算法
itemsets, rules = apr(transactions, min_support=0.05,  min_confidence=0.2)
print("*"*20,'频繁项集','*'*20)
print(itemsets)
print("*"*20,'关联规则','*'*20)
print(rules)