import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing
import numpy as np
from sklearn.preprocessing import LabelEncoder 
from sklearn import metrics

def best(train,row):
    flag = 2
    SCS_best = -1
    for i in range(2,row+1):
        kmeans = KMeans(n_clusters= i,max_iter=300)
        kmeans.fit(train)
        predict = kmeans.predict(train)
        SCS_now = metrics.silhouette_score(train, predict, metric='euclidean')
        #print("分为%d组时，轮廓系数为%s"%(i,SCS_now))
        if SCS_now > SCS_best:
            SCS_best = SCS_now
            flag = i
    #print("最佳分组是分为：%d 组"%(flag))
    return flag

def GetKMeans(data,train,num):
    kmeans = KMeans(n_clusters= num,max_iter=300)
    kmeans.fit(train)
    predict_x = kmeans.predict(train)
    #print(predict_x)
    result_x = pd.concat((data,pd.DataFrame(predict_x)),axis=1)
    #print(result_x)
    
    #返回车型名称和对应的分组情况
    df = pd.DataFrame(columns=['CarName','group'])
    df.CarName = data.CarName
    df.group = predict_x
    return df
    

def main():
    data = pd.read_csv('./CarPrice_Assignment.csv',encoding='gbk')
    #去除不需要计算的维度列
    train = data.drop(['car_ID','CarName'],axis=1)
    #LabelEncoder 
    le = LabelEncoder() 
    train['fueltype'] = le.fit_transform(train['fueltype']) 
    train['aspiration'] = le.fit_transform(train['aspiration']) 
    train['doornumber'] = le.fit_transform(train['doornumber']) 
    train['carbody'] = le.fit_transform(train['carbody']) 
    train['enginelocation'] = le.fit_transform(train['enginelocation']) 
    train['drivewheel'] = le.fit_transform(train['drivewheel']) 
    train['enginetype'] = le.fit_transform(train['enginetype']) 
    train['cylindernumber'] = le.fit_transform(train['cylindernumber']) 
    train['fuelsystem'] = le.fit_transform(train['fuelsystem']) 
    #0-1规范化
    min_max_scaler=preprocessing.MinMaxScaler()
    train=min_max_scaler.fit_transform(train)
    row = train.shape[0]-1
    
    #求解最佳分组数量
    group_num = best(train,row)
    print('最佳分类数目为：%s'%group_num)

    #按最佳分组数进行聚类，获取车型名称和对应的分组值，放入df中
    df = GetKMeans(data,train,group_num)
    #print(df)
    
    #找到包含特定字段的车型信息，包含车型名称和对应的分组值，放入df_filter中
    brand = 'volkswagen'
    bool = df.CarName.str.contains(brand)
    filter_data = df[bool]
    df_filter = pd.DataFrame(columns = ['CarName','group'])
    df_filter.CarName = filter_data.CarName
    df_filter.group = filter_data.group
    #print(df_filter)
    
    #对于df_filter中的每一个值，在df中查找相同group值下的CarName名称，并显示
    for j in df_filter['group']._stat_axis.values:
        x = df_filter.loc[j,'group']
        print('车型%s的竞品为:'%df_filter.loc[j,'CarName'])
        
        for i in df['group']._stat_axis.values:
            item = df.loc[i,'group']
            if item == x:
                if df_filter.loc[j,'CarName']!=df.loc[i,'CarName']:
                    print(df.loc[i,'CarName'])
            
    
if __name__ == '__main__':
    main()