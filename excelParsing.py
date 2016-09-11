from xlrd import open_workbook
import pymongo
import datetime

#创建一个用于读取sheet的生成器,依次生成每行数据,row_count 用于指定读取多少行, col_count 指定用于读取多少列
def readsheet(s, row_count=-1, col_count=-1):#
    # Sheet 有多少行
    nrows = s.nrows
    # Sheet 有多少列
    ncols = s.ncols
    row_count = (row_count if row_count > 0 else nrows)
    col_count = (col_count if col_count > 0 else ncols)
    row_index = 0
    while row_index < row_count:
        yield [s.cell(row_index, col).value for col in range(col_count)]
        row_index += 1

# 读取Excel中所有的Sheet，格式化每行为dict格式,写入DB
def format_sheet(workbook):
    for s in wb.sheets():
        # 只读取每个Sheet的前10行，前10列(当然你要确保,你的数据多余10行，且多余10列)
        sheet = readsheet(s)
        first_row = next(sheet)
        for row in  sheet:
            format_row = dict(zip(first_row, row))
            format_row['机房'] = format_row['机房'].upper()
            network_device.insert_one(format_row)
            #print(format_row)
        print('done!')

client = pymongo.MongoClient('localhost', 27017)
resource_pool = client['Resource_Pool']
network_device = resource_pool['Network_Device'+'_'+ datetime.datetime.now().strftime("%Y-%m-%d")]
wb = open_workbook('D:\Python35\Codes\网络设备.xlsx') #打开Excel文件
format_sheet(wb)