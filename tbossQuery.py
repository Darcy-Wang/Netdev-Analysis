import requests
import hashlib
import json
import pymongo
from datetime import datetime

node1 = [{"sn":"2102350JAS10F6000184"}]
node = [{"deviceType":"NETWORK_DEVICE", "nodeGroup":"network-spare"}]
apiName = 'netws'
apiCode = '02cc471774bb7ad3'
timestamp = datetime.now().strftime('%Y%m%d%H%M')



def getFromTboss(node, skip=0, take=1000):
    Tboss_url = 'https://tboss.alibaba-inc.com/tboss/web/api/resourcepool/queryResourcePoolList.json'
    # _username = 'infradata'

    params = {
        'node': json.dumps(node),
        'skip': skip,
        'take': take,
        'apiName': apiName,
        'timestamp': timestamp,
        'signature': tbossSign(apiName, timestamp, apiCode)
    }
    try:
        resp = requests.post(Tboss_url, params=params, verify=True)
        print(resp.url)
        if resp.status_code != 200:
            print('Error! Tboss API status_code is ' + str(resp.status_code))
        return resp.json()
        # if resp.status_code == 200:
        #     if resp.json().get('code'):  # 存在错误 抛出异常
        #         print('存在错误')
        #         return []
        #     else:
        #         return resp.json().get('result')
        # else:
        #     print('not 200=' + str(resp.status_code))
        #     return []
    except Exception as e:
        print('error=' + str(e))
        return []


def tbossSign(apiName, timestamp, Code):
    unencrypted = apiName.encode("utf-8")  +timestamp.encode("utf-8") + Code.encode("utf-8")
    m1 = hashlib.md5(unencrypted)
    # print(unencrypted)
    # print(m1.hexdigest())
    return m1.hexdigest()


def formatResult(node, skip=0, take=1000):
    data_org = getFromTboss(node, skip, take)
    print(data_org)

    if (data_org['hasError'] == False):
        if data_org['content']['success'] == True:
            print('Get result success!')
            for k1, v1 in data_org.items():

                if (k1 == 'content'):
                    # print(k1, v1)
                    for k2, v2 in v1.items():
                        if (k2 == 'data'):
                            data = v2
            if data:
                # print('查询到设备数量为' + str(len(data)))
                formatData = data
                return formatData
            else:
                formatData = {}
                return formatData
        else:
            print('The result has Error!')
    else:
        print('The result has Error!')

def getFormRes(node):
    skip = 0
    take = 1000
    data_format = formatResult(node)
    data_new = data_format
    while True:
        if len(data_new) == 1000:
            skip += 1000
            data_new = formatResult(node, skip, take)
            data_format = data_format + data_new

        else:
            break
    return data_format

def tboss2db():
    """
    将存入的数据数据进行修正，然后存入数据库。
    :param data_org:
    :return:
    """
    data_format = getFormRes(node)
    print('查询结果设备数量为', len(data_format))

    client = pymongo.MongoClient('localhost', 27017)
    ArmoryDB = client['TbossDB']
    network_device = ArmoryDB['TbossNetwork_Device' + '_' + datetime.now().strftime("%Y-%m-%d")]
    print('Saving db begins...')
    network_device.insert_many(data_format)
    print("Saving db completed!")



if __name__ == '__main__':
    getFormRes(node1)
    # for i in data_format:
    #     print(i['sn'])
