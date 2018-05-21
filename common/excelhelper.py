# coding:utf-8
import os
import xlwt
import xlrd
from xlutils.copy import copy


def get_file_path(file_dir, file_name):
    file_path = u'{}{}.xls'.format(file_dir, file_name)
    return file_path


def opend(file_name='default', file_dir=''):
    file_path = get_file_path(file_dir, file_name)
    #  formatting_info=True
    oldWb = xlrd.open_workbook(file_path)
    return oldWb


def create(fields, file_name='default', file_dir=''):
    '''
        创建excel
    '''
    try:
        file_path = get_file_path(file_dir, file_name)
        have = os.path.exists(file_path)
        if have:
            print(u'{}文件已经存在'.format(file_path))
            return
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'Sheet1')
        for index in range(len(fields)):
            field_name = fields[index]
            ws.write(0, index, field_name)
            wb.save(file_path)
    except Exception as ex:
        print('excel helper create err:', ex)


def append(datas, file_name='default', file_dir=''):
    '''
        excel追加数据
    '''
    try:
        oldWb = opend(file_name, file_dir)
        oldWbS = oldWb.sheet_by_index(0)
        newWb = copy(oldWb)
        newWs = newWb.get_sheet(0)
        inserRowNo = oldWbS.nrows
        for index in range(len(datas)):
            newWs.write(inserRowNo, index, datas[index])
        # for rowIndex in range(inserRowNo, oldWbS.nrows):
        #     for colIndex in range(oldWbS.ncols):
        #         newWs.write(rowIndex + 1, colIndex,
        #                     oldWbS.cell(rowIndex, colIndex).value)
        file_path = get_file_path(file_dir, file_name)
        newWb.save(file_path)
    except Exception as ex:
        print('excel helper append err:', ex)


def appends(datas, file_name='default', file_dir=''):
    '''
        excel追加数据
    '''
    try:
        oldWb = opend(file_name, file_dir)
        oldWbS = oldWb.sheet_by_index(0)
        newWb = copy(oldWb)
        newWs = newWb.get_sheet(0)
        inserRowNo = oldWbS.nrows
        for item in datas:
            try:
                values = list(item.values())
                for index in range(len(values)):
                    newWs.write(inserRowNo, index, values[index])
                inserRowNo = inserRowNo + 1
            except Exception as ex:
                print('excel helper append write item err:', ex)
        file_path = get_file_path(file_dir, file_name)
        newWb.save(file_path)
    except Exception as ex:
        print('excel helper append err:', ex)


def read(colnameindex=0,
         sheet_name=u'Sheet1',
         file_name='default',
         file_path='',
         sheet_index=None):
    '''
        excel列表读取
    '''

    data = opend(file_name, file_path)
    if sheet_index is not None and isinstance(sheet_index, int):
        table = data.sheet_by_index(sheet_index)
    else:
        table = data.sheet_by_name(sheet_name)
    nrows = table.nrows
    colnames = table.row_values(colnameindex)
    datas = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            datas.append(app)
    return datas
