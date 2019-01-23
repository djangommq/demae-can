
import csv
import json
import requests

import os

from get_blockcodes import log, shop_field, save_item, block_field, sleep_seconds

VERSION = 'latest'
WEB_NAME = 'demae-can'

shop_field_Detail=[
    "shopId",
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


def get_shops(block_code,shopId):
    url = "https://japi2.demae-can.com/DemaeAPI/shop/getShopDetail"
    body = {
      "shopId": shopId,
      "blockCode": block_code,
      "author": "android3",
      "ifVersion": "4.17",
      "encryptId": "12d4f9e5109a362fc7c757997328b712a17b85435399b3fe00ccec8e2258db75",
    }
    headers = {
        'carrierName': 'android3',
        'uName': 'PLK-TL01H',
        'osVersion': 'Android5.0.2',
        'User-Agent': 'RestSharp/105.2.3.0',
        'Accept': 'application/json, application/xml, text/json, text/x-json, text/javascript, text/xml, application/json, text/json, text/x-json, text/javascript',
        'Content-Type': 'application/json',
        'Content-Length': '207',
        'Host': 'japi2.demae-can.com',
        'Accept-Encoding': 'gzip, deflate',
    }

    response = requests.request("POST", url, data=json.dumps(body),headers=headers)
    sleep_seconds()
    result = json.loads(response.text)
    if result.get('code') == 'S1007':
        log('{}错误,该地区暂未开通'.format(block_code))
        result = None
    elif result.get('code') != '0000':
        log('{}错误,原因其他'.format(block_code))
        result = None
    return result


# res 中存储着一个地区的所有商店
def parse_shop(rest_info):
    rest_dict={}
    for detail in shop_field_Detail:
        if type(rest_info[detail])==type('ABC'):
            rest_info[detail]=rest_info[detail].replace('\n', '').replace('\r','')
        rest_dict[detail]=rest_info[detail]

    filedir_d=os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/{}/'.format(VERSION, WEB_NAME))
    filename_d=os.path.join(filedir_d,'shop_detail.csv')
    if not os.path.exists(filename_d):
        with open(filename_d,'w',encoding='utf-8',newline='')as f:
            writer=csv.DictWriter(f,fieldnames=shop_field_Detail)
            writer.writeheader()

    with open(filename_d, 'a', encoding='utf-8', newline='')as f:
        writer = csv.DictWriter(f, fieldnames=shop_field_Detail)
        writer.writerow(rest_dict)



if __name__ == '__main__':
    filedir=os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/{}/'.format(VERSION, WEB_NAME))
    filename=os.path.join(filedir,'shops_deduplicate.csv')
    with open (filename,'r',encoding='utf-8',newline='')as f:
        reader=csv.DictReader(f,fieldnames=shop_field)
        result=[]
        for row in reader:
            if reader.line_num==1:
                continue
            else:
                result.append(dict(row))
    i=0
    for rest in result:
        print(i)
        try:
          res=get_shops(rest['blockCode'],rest['shopId'])
          Baseinfo=res['shopBaseInfo'][0]
          rest_info=dict(res,**Baseinfo)
        except TimeoutError as e:
            log('{} :请求超时'.format(rest['blockCode']))
            continue
        except Exception as e:
            log('其他异常', e)
            continue

        parse_shop(rest_info)
        i += 1
