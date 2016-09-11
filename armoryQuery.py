import requests
import pymongo
from datetime import datetime

def get_from_armory(target, select, num, start, q):
    armory_url = 'http://a.alibaba-inc.com/page/api/free/opsfreeInterface/search.htm'
    _username = 'infradata'
    data = {
        '_username': _username,
        'from': target,
        'select': select,
        'num': num,
        'start': start,
        'q': q
    }
    try:
        resp = requests.post(armory_url, data=data, verify=False)
        #print('armory API status_code:' + str(resp.status_code))
        if resp.status_code == 200:
            if resp.json().get('code'):  # 存在错误 抛出异常
                print('存在错误,原因是：', resp.json().get('code'))
                return []
            else:
                return resp.json().get('result')
        else:
            print('not 200=' + str(resp.status_code))
            print('not 200=', resp.url)
            return resp.json().get('result')
    except Exception as result:
        print(result.__class__)
        if hasattr(result, status_code):
            print('error occur! the status code is ' + str(result.status_code))

        return []

def get_netdev(nodegroup , select, query, num=0):
    """
    首先使用nodegroup进行第一次条件查询，然后将返回的sn进行第二次API查询，最终根据条件返回过滤结果（list）

    :param nodegroup:
    :param select:
    :param query:
    :param num:
    :return:
    """
    target = 'device'
    num = 0
    start = 0
    first_select = 'sn'
    first_num = 0
    first_start = 0

    if isinstance(nodegroup,str):
        qgroup = "nodegroup in ('{}')".format(nodegroup)
    elif nodegroup == None:
        qgroup = "device_type = 'network_device'"
        return get_from_armory('network', select, num, start, query)

    else :
        nodegroup = ','.join(["'" + n + "'" for n in nodegroup])
        qgroup = "nodegroup in ({})".format(nodegroup)

    first_data = get_from_armory(target, first_select, first_num, first_start, qgroup)

    #print('First query nums are '+str(len(first_data)))

    if len(first_data) == 0:
        return first_data

    elif len(first_data) > 1:
        sn = ','.join(["'" + str(i['sn']).strip() + "'" for i in first_data])
    else:
        sn = ''.join(["'" + i['sn'] + "'" for i in first_data])
    if query:
        fullquery = query + "and sn in({})".format(sn)
    else:
        fullquery = "sn in({})".format(sn)
    # print(fullquery)
    data = get_from_armory('network', select, num, start, fullquery)
    return data

def armory2db(data_org):
    """
    将存入的数据数据进行修正，然后存入数据库。
    :param data_org:
    :return:
    """
    for i in allData:
        i["manifest"] = i[".manifest"]
        i.pop(".manifest")

    client = pymongo.MongoClient('localhost', 27017)
    ArmoryDB = client['ArmoryDB']
    network_device = ArmoryDB['Network_Device' + '_' + datetime.now().strftime("%Y-%m-%d")]
    print('Saving db begins...')
    network_device.insert_many(allData)
    print("Saving db completed!")


if __name__ == '__main__':

    offline_nodegroup = ['network-arrive', 'network-buffer', 'network-construction']
    spare_nodegroup = ['network-spare']
    scrap_nodegroup = ['network-scrap', 'network-deleted']
    onlineQuery = "app_state in ('working_powersaving','working_online','working_preonline')"
    select = 'sn,nodename,model,dns_ip,manufacturer,app_state,netlogic_site,dsw_cluster,net_pod,logic_pod,site,use_state,manifest,networkGroup,is_vm'
    onlineData = get_netdev(None, select, onlineQuery)
    offlineData = get_netdev(offline_nodegroup, select, None)
    spareData = get_netdev(spare_nodegroup, select, None)
    scrapData = get_netdev(scrap_nodegroup, select, None)
    allData = get_netdev(None, select, None)
    armory2db(allData)


    print('在线设备数(含逻辑设备)：'+ str(len(onlineData)))
    print('逻辑设备数：'+ str(len([i for i in onlineData if i['is_vm'] == 1])))
    print('在线物理设备数：'+ str(len([i for i in onlineData if i['is_vm'] == 0])))
    print('离线物理设备数：'+ str(len(offlineData)))
    print('备件物理设备数：'+ str(len(spareData)))
    print('报废中物理设备数：'+ str(len(scrapData)))
    print('设备总数(含逻辑设备)：'+ str(len(allData)))
    print('设备总数(不含逻辑设备)：'+ str(len([i for i in allData if i['is_vm'] == 0])))

    # 测试代码
    # for i in range(10):
    #     print(allData[i])







