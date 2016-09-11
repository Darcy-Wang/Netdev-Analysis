import pymongo
import datetime

'''
分析tboss中3.5,4.0,4.1主流架构DSW、PSW、ASW型号的库存型号。
输入：TBOSS资源池设备数据库，查询型号（默认为主流架构AVL型号）,应用分组(默认为库存分组)
筛选条件：锁定状态为未锁定，预录入状态为未录入，设备型号在架构AVL中，分组为network-construction,network-arrive,network-buffer,机房为主站机房
各型号库存数量
衍生功能：展示水位线
'''
default_goups = ['network-construction','network-arrive','network-buffer']
default_models = ['LS-9804','LS-5800-54S','LS-9810','LS-6800-54QF', 'LS-5820V2-52QF', 'CE6851-48S6Q-HI', \
                  'CE12816-AC','CE12804S-AC1','LS-12516X-AF','N6004-B-24Q','N2K-C2248TP-E-1GE', 'N2K-C2348UPQ']
mainsite_idc = ['ET2','ET15','EU13','EM14','CM3','ZTG','CM10','ZTH','ZTT','ZMF','HZLT','ET1','CM4','CM6','CM8','ZUE',\
               'ALI','TBC','HL','CM11','EU6','EM21','EW9','NU8','NT12','CM5','CM9','NU20','BTC','CM12','NU16',\
               'NU17','BJL1','BJL2','BJS1','BJW1','BJM1','BJC1','NJT','QDU','ST3','ST4','SU18','MEG','NA61','NA62','AM5']


client = pymongo.MongoClient('localhost', 27017)
resource_pool = client['Resource_Pool']
network_device = resource_pool['Network_Device'+'_'+ '2016-08-24']
print('network_device sheet counts are {}'.format(network_device.count()))

def repertory_device_query(sheet, models=default_models, goups=default_goups, idc = mainsite_idc, sn=False):

    for m in models:
        query_res = sheet.find({'锁定': '未锁定', '预录入': '否', '锁定人':'无','分组': {'$in': goups}, '机房':{'$in': idc}, '型号': m}, {'_id': 0, 'SN': 1, '型号': 1})
        data = {m:query_res.count()}
        print('{} counts are {}'.format(m, query_res.count()))
        if sn:
            print('sn numbers are:')
            for dev in query_res:
                print(dev['SN'])
        else:
            pass



repertory_device_query(network_device,models=['LS-6800-54QF'], idc=mainsite_idc, sn=True)