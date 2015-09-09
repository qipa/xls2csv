# encoding: utf-8

import os,sys,inspect,re
import xdrlib,xlrd

reload(sys)
sys.setdefaultencoding("utf-8")

#分割符
C_SPACE = ","
#结束符
C_END = "\n"

#获取脚本文件的当前路径
def cur_file_dir():
    path = os.path.realpath(sys.path[0])
    print path
    if os.path.isfile(path):
        print "exe"
        path = os.path.dirname(path)
        return os.path.abspath(path)
    else:
        print "文件"
        caller_file = inspect.stack()[1][1]
        return os.path.abspath(os.path.dirname(caller_file))

#搜索指定文件夹下面的文件（默认当前目录）
def find_file_by_pattern(pattern='.*', base=".", circle=True):  
    '''''查找给定文件夹下面所有 '''
    re_file = re.compile(pattern)
    if base == ".":
        base = cur_file_dir()
    print "开始搜索文件夹：",base

    final_file_list = []
    cur_list = os.listdir(base)  
    for item in cur_list:
        # print item
        if item == ".svn":
            continue
          
        full_path = os.path.join(base, item)

        if full_path.startswith("~"):
            continue

        if full_path.endswith(".xlsx") or full_path.endswith(".xls"):
            print "in:" + full_path
            bfile = os.path.isfile(item)
            if os.path.isfile(full_path):
                if re_file.search(full_path):
                    final_file_list.append(full_path)  
            else:
                final_file_list += find_file_by_pattern(pattern, full_path)

    '''返回文件列表'''
    return final_file_list


#打开excel
def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)


#根据索引获取Excel表格中的数据 参数:file：Excel文件路径, colnameindex：表头列名所在行的索引, by_index：表的索引
def excel_table(file='file.xls', colnameindex=0 , path='dir'):
    data = open_excel(file)
    for table in data.sheets():
        sheet_name = table.name.replace(" ", "_")
        if not sheet_name.startswith("output_"):
            continue
        sheet_name = sheet_name[7:]
        nrows = table.nrows #行数
        ncols = table.ncols #列数
        rowlist = []
        # print heads
        '''开始读取数据'''
        for rownum in range(colnameindex, nrows):
            rowdata = table.row_values(rownum)
            if rowdata:
                collist = []
                for i in range(ncols):
                    collist.append(rowdata[i])
                rowlist.append(collist)
        if len(rowlist)>0:
            savaToCSV(file, rowlist, path + "/" + sheet_name + ".csv" )

#保存csv文件
def savaToCSV(_file, _list, _path):
    filename = ""
    content = ""
    #生成文件内容
    for collist in _list:
        for i in range(len(collist)):
            v = collist[i]
            vstr = ""
            # print k,v
            if isinstance(v, float) or isinstance(v, int):
                vstr = str(int(v))
            else:# elif isinstance(v, str):
                vstr = v
            if i > 0:
                content = content + C_SPACE
            content = content + vstr
        content = content + C_END

    #写文件
    if len(_path)>0 and len(content)>0:
        print "out:" + _path
        file_object = open(_path, 'w')
        file_object.write(content)
        file_object.close()


def main():
    if len(sys.argv) < 3:
        sys.exit('''usage: xls2csv.py excel_name output_path''')
    filename = sys.argv[1]
    output_path = sys.argv[2]
    excel_table(filename , 0 , output_path)

if __name__=="__main__":
    main()
