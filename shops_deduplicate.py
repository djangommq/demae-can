import csv
import os
from get_shops import VERSION,WEB_NAME

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

def get_all_info():
  filename=os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/{}/shops.csv'.format(VERSION, WEB_NAME))
  result={}
  with open(filename,'r',encoding='utf-8',newline='')as f:
    reader=csv.DictReader(f,fieldnames=shop_field)
    for row in reader:
      if reader.line_num==1:
        continue
      else:
        result[row.get('shopId')]=dict(row)

  return result


def save_info(items):
  filename=os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/{}/shops_deduplicate.csv'.format(VERSION, WEB_NAME))
  if not os.path.exists(filename):
    with open(filename,'w',encoding='utf-8',newline='')as f:
      writer=csv.DictWriter(f,fieldnames=shop_field)
      writer.writeheader()

  with open(filename,'a',encoding='utf-8',newline='')as f:
      writer = csv.DictWriter(f, fieldnames=shop_field)
      for row in items:
        writer.writerow(row)


if __name__ == '__main__':
    result=get_all_info()
    save_info(result.values())




