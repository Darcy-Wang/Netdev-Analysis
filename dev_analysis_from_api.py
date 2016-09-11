import pymongo
import datetime

'''
1、在线设备数（online、preonline、powersaving）
2、库存设备数（arrive、construction、buffer、spare、scrap、deleted）
3、在线率统计（主站设备在线率）
3、四大供应商设备数(cisco, huawe, juniper, h3c)
4、4.1，4.0,3.5主要设备buffer数量，水位图（新到货设备、锁定设备需排除）
5、设备库存3个月周转率（需要标识到货超过3个月的设备）
'''

client = pymongo.MongoClient('localhost', 27017)
ArmoryDB = client['ArmoryDB']
network_device = ArmoryDB['Network_Device'+'_'+  datetime.datetime.now().strftime("%Y-%m-%d")]
print(network_device.find().count())

# for i in network_device.find({"manufacturer": "Cisco"}):
#     print(i['model'])

print(network_device.find({"manufacturer": {'$regex':'(?i)Cisco'}}).count())
print(network_device.find({"manufacturer": {'$regex':'(?i)Huawei'}}).count())
print(network_device.find({"manufacturer": {'$regex':'(?i)H3C'}}).count())
print(network_device.find({"manufacturer": {'$regex':'(?i)Juniper'}}).count())
print(network_device.find({"manufacturer": {'$regex':'(?i)Avocent'}}).count())
print(network_device.find({"manufacturer": {'$regex':'(?i)netscaler'}}).count())
print(network_device.find({"manufacturer": {'$regex':'(?i)Citrix'}}).count())
# for i in network_device.find({"manufacturer": {'$regex':'(?i)netscaler'}}):
#     print(i['sn'])
for i in network_device.find({"sn": {'$regex':'(?i)696CV1XXRM'}}):
    print(i)