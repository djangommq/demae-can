## demae-can


## 基本情况
1. 起始于： 2018年11月   
2. 相关国家和地区： 日本


## API的获取
- 破解方法  
抓包获得:   
    app详情可以见代码  
- 获取逻辑:   
    1. 先得到block_code, 区域为国家→地方(area)→县(prefecture)→市(city)→区(block_code), 共请求4次
    2. 使用block_code去请求shoplist

## 代码地址
[gitlab: https://gitlab.yunfutech.com/uber_crawler/demae-can.git](https://gitlab.yunfutech.com/uber_crawler/demae-can.git)  


## 进展
2018-11-18: 提交第一版数据  
2018-12-03: 更新后api不能使用, 要求升级, 重新抓包  
            之后如果又出现要求升级, 可以先修改post中的version参数试试

## 追加要求


## 使用说明

**20180831**
1. block_code一次获取, 保存在input/block_codes.csv
2. 直接运行get_shops.py
    ```python
    python3 get_shops.py
    ```
3. 输出结果  
    ```python
    ../../crawlerOutput/latest/shops.csv
    ```
4. 数据去重
    ```
        运行去重脚本
        python3 shops_deduplicate.py
    ```
    
5. 运行get_shops_detail.py
    ```python
    python3 get_shops_detail.py
    ```

6.输出结果
    ```python
    ../../crawlerOutput/latest/shop_detail.csv
    ```
7. 数据上传
    ```
    上传shop_detail.csv
    
    ```


