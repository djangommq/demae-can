
import csv
import json
import requests

import os

from get_blockcodes import log, shop_field, save_item, block_field, sleep_seconds

VERSION = 'latest'
WEB_NAME = 'demae-can'


def load_block_codes():
    file_path = os.path.join(os.path.dirname(__file__), 'input/blockcodes.csv')
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        csv_f = csv.DictReader(f, fieldnames=block_field)
        result = []
        for row in csv_f:
            if csv_f.line_num == 1:
                continue
            result.append(dict(row))
    return result


def get_shops(block_code, page=1):
    url = "https://japi2.demae-can.com/DemaeAPI/shop/getShopList"
    body = {
        "blockCode": block_code,
        "page": page,
        "author": "android3",
        "ifVersion": "4.17",
        "encryptId": "12d4f9e5109a362fc7c757997328b712a17b85435399b3fe00ccec8e2258db75",
    }
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
        'Postman-Token': "7d0364e7-0adf-4373-ad7f-5cc2789b4f3a"
    }

    response = requests.request("POST", url, data=json.dumps(body), headers=headers, timeout=2)
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
def parse_shop(res):
    # 获取所有商店
    shop_list = res.get('shopList')
    with_out_fields = [
        'addressName',
        'blockCode'
    ]
    for shop in shop_list:
        item = {}
        for head in shop_field:
            if head in with_out_fields:
                item[head] = res.get(head)
            else:
                item[head] = shop.get(head)
        save_item('shop', item)


def save_has_got(id):
    has_got_dir = os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/{}'.format(VERSION, WEB_NAME))
    has_got_name = 'has_got_codes.txt'
    has_got_path = os.path.join(has_got_dir, has_got_name)
    if not os.path.exists(has_got_dir):
        os.makedirs(has_got_dir)
    with open(has_got_path, 'a', encoding='utf-8') as f:
        f.write(id + '\n')


def load_has_got():
    has_got_dir = os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/{}'.format(VERSION, WEB_NAME))
    has_got_name = 'has_got_codes.txt'
    has_got_path = os.path.join(has_got_dir, has_got_name)
    result = []
    if not os.path.exists(has_got_path):
        result = []
    else:
        with open(has_got_path, 'r', encoding='utf-8') as f:
            for row in f.readlines():
                result.append(row.strip())
    return result


if __name__ == '__main__':
    # block_codes:{'blockCode': '01662001000', 'postNo': '0881113', 'addressName': '愛冠', 'shopCount': '1', 'city': '厚岸郡\u3000厚岸町', 'prefectureCode': '01', 'prefecture': '北海道'}
    block_codes = load_block_codes()
    has_got_codes = load_has_got()
    for i in block_codes:
        block_code = i.get('blockCode')
        if block_code in has_got_codes:
            continue
        log('开始请求block_code:{} 的餐馆'.format(block_code))
        try:
            res = get_shops(block_code)
        except TimeoutError as e:
            log('{} :请求超时'.format(block_code))
            continue
        except Exception as e:
            log('其他异常', e)
            continue
        if res is None:
            continue
        parse_shop(res)
        shop_page_count = res.get('shopLastPage')
        for page in range(2, shop_page_count+1):
            try:
                res = get_shops(block_code,page)
            except TimeoutError as e:
                log('{} :请求超时'.format(block_code))
                continue
            except Exception as e:
                log('其他异常', e)
                continue
            if res is None:
                continue
            parse_shop(res)
        save_has_got(block_code)
