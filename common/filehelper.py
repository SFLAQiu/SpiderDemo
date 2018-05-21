# coding:utf-8
import os


def file_names(file_dir, extension):
    '''
        获取目录下的所有符合拓展类型的文件
    '''
    match_files = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.{0}'.format(extension):
                match_files.append(os.path.join(root, file))
    return match_files


def file_remove(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

