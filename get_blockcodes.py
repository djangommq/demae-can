import csv
import json
import requests
import random
import os
from time import sleep

VERSION = 'latest'
WEB_NAME = 'demae-can'

block_field = [
    "blockCode",
    "postNo",
    "addressName",
    "shopCount",
    "city",
    "prefectureCode",
    "prefecture",
]

shop_field = [
    "addressName",
    "blockCode",
    "shopId",
    "shopName",
    "prFlg",
    "isEvaluation",
    "evaluationPoint",
    "shopStatus",
    "isOpen",
    "isClose",
    "isNear",
    "isNetReceiptOverTime",
    "isNetReceiptStopping",
    "isStop",
    "isUrgencyStop",
    "shopSts",
    "isAccepting",
    "waitTime",
    "minOrderCondition",
    "minOrderPrice",
    "minOrderPriceParam",
    "charge",
    "pointGrantRate",
    "tpointBaseRate",
    "pointGrantFlg",
    "pointUseFlg",
    "dispPayCardFlg",
    "dispPayAmazonFlg",
    "dispLinePayFlg",
    "dispMadonnaPayFlg",
    "dispAuCarrierPayFlg",
    "dispSbCarrierPayFlg",
    "otherLink",
    "isNotEmptyOtherLink",
    "hours",
    "shopEvalCount",
    "shopPrComment",
]

shop_field_Detail=[
    "shopId",
    "shopLogoImageUrl",
    "shopName",
    "addressName",
    "blockCode",
    "amenity",
    "isEvaluation",
    "evaluationPoint",
    "evaluationPointTaste",
    "evaluationPointPrice",
    "evaluationPointVolume",
    "evaluationPointService",
    "evaluationPointTime",
		"hours",
		"holiday",
		"shopAddress",
		"charge",
		"minOrderCondition",
		"minOrderPrice",
		"minOrderPriceParam",
		"waitTime",
		"pointGrantRate",
		"tpointBaseRate",
		"pointGrantFlg",
		"pointUseFlg",
		"isDispCouponImg",
		"status",
		"isOpen",
		"isEnableFreeCall",
		"freeCallType",
		"freeConsultDialMb",
		"shopSts",
		"isSuspend",
		"isOutOfOrderTime",
		"isSelectTimeZone",
		"dispPayCardFlg",
		"dispPayAmazonFlg",
		"dispLinePayFlg",
		"dispMadonnaPayFlg",
		"dispAuCarrierPayFlg",
		"dispSbCarrierPayFlg",
    "catchphrase",
    "attention",
    "shopInformation",
    "isFavorite",
    "chainNm",
    "genreTopCategory",
    "phoneNo",
    "shopPrefAddress",
    "cardTranShopId"
]



def log(*args):
    print(*args)
    log_dir = os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/log/{}/'.format(VERSION, WEB_NAME))
    log_name = 'demae-can.log'
    log_path = os.path.join(log_dir, log_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(log_path, 'a', encoding='utf-8') as f:
        print(*args, file=f)


def sleep_seconds():
    sleep(random.randint(0,1))


def get_area():
    url_area = 'https://japi2.demae-can.com/DemaeAPI/address/getArea'
    body = {
        "author": "android3",
        "ifVersion": "4.16",
        "encryptId": "1a28d5a2b27383e0e97c586e3c4e6a39a17b85435399b3fe00ccec8e2258db75"
    }
    headers1 = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url_area, data=json.dumps(body), headers=headers1, timeout=2)
    sleep_seconds()
    result = json.loads(response.text)
    if result.get('code') != '0000':
        print(result)
        result = None
    return result


def get_prefecture(area_code):
    url_prefecture = 'https://japi2.demae-can.com/DemaeAPI/address/getPrefecture'
    body = {
        "areaCode": area_code,
        "author": "android3",
        "ifVersion": "4.16",
        "encryptId": "1a28d5a2b27383e0e97c586e3c4e6a39a17b85435399b3fe00ccec8e2258db75"
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url_prefecture, data=json.dumps(body), headers=headers, timeout=2)
    sleep_seconds()
    result = json.loads(response.text)
    if result.get('code') != '0000':
        print(result)
        result = None
    return result


def get_block_code_by_city(code):
    url_search_block = 'https://japi2.demae-can.com/DemaeAPI/address/searchBlock'
    headers = {
        'carrierName': "android3",
        'uName': "PLK-TL01H",
        'osVersion': "Android5.0.2",
        'User-Agent': "RestSharp/105.2.3.0",
        'Accept': "application/json, application/xml, text/json, text/x-json, text/javascript, text/xml, application/json, text/json, text/x-json, text/javascript",
        'Content-Type': "application/json",
        'Content-Length': "202",
        'Host': "japi2.demae-can.com",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache",
    }
    body = {
        "kind": "city",
        "blockCode": code,
        "author": "android3",
        "ifVersion": "4.16",
        "encryptId": "1a28d5a2b27383e0e97c586e3c4e6a39a17b85435399b3fe00ccec8e2258db75"
    }
    response = requests.request("POST", url_search_block, data=json.dumps(body), headers=headers, timeout=2)
    sleep_seconds()
    result = json.loads(response.text)
    if result.get('code') != '0000':
        print(result)
        result = None
    return result


def get_block_code_by_name(code):
    url_search_block = 'https://japi2.demae-can.com/DemaeAPI/address/searchBlock'
    headers = {
        'carrierName': "android3",
        'uName': "PLK-TL01H",
        'osVersion': "Android5.0.2",
        'User-Agent': "RestSharp/105.2.3.0",
        'Accept': "application/json, application/xml, text/json, text/x-json, text/javascript, text/xml, application/json, text/json, text/x-json, text/javascript",
        'Content-Type': "application/json",
        'Content-Length': "202",
        'Host': "japi2.demae-can.com",
        'Accept-Encoding': "gzip, deflate",
        'cache-control': "no-cache",
    }
    body = {
        "kind": "name",
        "blockCode": code,
        "author": "android3",
        "ifVersion": "4.16",
        "encryptId": "1a28d5a2b27383e0e97c586e3c4e6a39a17b85435399b3fe00ccec8e2258db75"
    }
    response = requests.request("POST", url_search_block, data=json.dumps(body), headers=headers, timeout=2)
    sleep_seconds()
    result = json.loads(response.text)
    if result.get('code') != '0000':
        print(result)
        result = None
    return result


def save_item(type, data):
    file_dir = os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/{}/'.format(VERSION, WEB_NAME))
    if type == 'block_code':
        file_name = 'blockcodes.csv'
        head = block_field
    elif type == 'shop':
        file_name = 'shops.csv'
        head = shop_field
    else:
        return 0

    file_path = os.path.join(file_dir, file_name)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            f_csv = csv.DictWriter(f, fieldnames=head)
            f_csv.writeheader()
    with open(file_path, 'a', newline='', encoding='utf-8') as fw:
        fw_csv = csv.DictWriter(fw, fieldnames=head)
        for k, v in data.items():
            data[k] = str(v).replace('\n', ' ').replace('\r', ' ')
        fw_csv.writerow(data)


def parse_block_code(res):
    addressInfoLists = res.get('addressInfoList')
    # 解析出第一层blockcode
    result = []
    for list in addressInfoLists:
        addressInfos = list.get('addressInfo')
        for info in addressInfos:
            block_code = info.get('blockCode')
            result.append(block_code)
    return result


def parse_item(res):
    addressInfoLists = res.get('addressInfoList')
    city = res.get('city')
    prefectureCode_tmp = res.get("prefectureCode")
    prefecture_tmp = res.get('prefecture')
    for list in addressInfoLists:
        addressInfos = list.get('addressInfo')
        for info in addressInfos:
            item = {
                "blockCode": info.get("blockCode"),
                "postNo": info.get("postNo"),
                "addressName": info.get("addressName"),
                "shopCount": info.get("shopCount"),
                "city": city,
                "prefectureCode": prefectureCode_tmp,
                "prefecture": prefecture_tmp
            }
            save_item('block_code', item)
            # log('解析出: ', item)


if __name__ == '__main__':
    res1 = get_area()

    # area_list = <class 'list'>: [{'areaCode': '0', 'areaName': '北海道'}, ...
    area_list = res1.get('areaList')
    # 解析出area_id
    log("area_code共有个数:", len(area_list))
    for area in area_list:
        area_code = area.get('areaCode')
        log('第一层: 开始请求area_code为{}'.format(area_code))
        try:
            res2 = get_prefecture(area_code)
        except Exception as e:
            log('错误请求area_code:', area_code)
            continue

        # <class 'list'>: [{'prefectureCode': '01000000000', 'prefecture': '北海道'}]
        prefectureList = res2.get('prefectureList')
        log("prefecture共有个数:", len(prefectureList))
        # 解析出prefecture_id
        for prefecture in prefectureList:
            prefecture_code = prefecture.get('prefectureCode')
            log('第二层: 开始请求prefecture_code为{}的block_code'.format(prefecture_code))
            try:
                res3 = get_block_code_by_city(prefecture_code)
            except Exception as e:
                log('错误请求prefecture:', prefecture_code)
                continue
            log('第一次解析block_code')
            block_codes = parse_block_code(res3)
            parse_item(res3)
            # for code in block_codes:
            #     log('第二次解析block_code')
            #     try:
            #         res4 = get_block_code_by_name(code)
            #     except Exception as e:
            #         log('错误请求block_code:', code)
            #         continue
            #     parse_item(res4)




