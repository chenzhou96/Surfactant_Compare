import os
import re
import numpy as np
from pathlib import Path

def _read_filenames(path: Path) -> list:
    """
    读取路径文件夹内所有csv文件名
    返回文件名构成的列表
    """

    filenames = os.listdir(path)

    # 只读取csv文件
    names_regex = re.compile(r'.csv$')
    name_output = re.compile(r'^output')
    for name in filenames[:]:
        if not names_regex.search(name.lower()):
            filenames.remove(name)
        if name_output.search(name.lower()):
            filenames.remove(name)

    return filenames

def _read_csv_data(path: Path, filename: str, column_index: int, skip_row: int) -> np.ndarray:
    """
    读取csv文件内第row行的数据
    返回ndarray数组
    """
    column_index -= 1
    try:
        path = str(path / filename)
        return np.loadtxt(path, delimiter=',', skiprows=skip_row, usecols=(column_index,)) # delimiter根据文件格式修改
    except:
        return None
    
def _read_PDA_max_data(path: Path, filename: str, skip_row: int) -> np.ndarray:
    """
    读取PDA光谱文件
    返回二维矩阵ndarray数组
    """
    try:
        path = str(path / filename)
        data = np.loadtxt(path, delimiter=',', skiprows=skip_row) # delimiter根据文件格式修改
        # data为二维数组 第一列为时间 其他列为不同波段的吸光度
    except:
        return None
    
    rows = data.shape[0]
    PDA_data = np.empty(rows)
    for index in range(rows):
        intensity = data[index][1:]
        PDA_data[index] = intensity.max() # 有待和手动处理的数据对比验证一下

    return PDA_data

def _zip_data(csvdata: np.ndarray, n = 1000) -> np.ndarray:
    """
    压缩数据量
    返回横坐标数据点为n的新数据
    """

    rows = len(csvdata)

    # 如果数据点不满n个 不需要进行压缩
    if n > rows:
        return csvdata

    zipdata = np.empty(n)
    for step in range(n):
        start = int(step * rows / n)
        end = int((step + 1) * rows / n)
        zipdata[step] = csvdata[start: end].mean()

    return zipdata

def read_all_data(path: Path, column_index: int, skip_row: int, flag: str) -> dict:
    """
    读取路径文件夹内所有csv文件内容
    返回文件名和文件内容构成的字典
    """
    
    alldata = dict()
    filenames = _read_filenames(path)
    if flag == 'nmr' or 'PDA_single':
        for filename in filenames:
            alldata[filename] = _zip_data(_read_csv_data(path, filename, column_index, skip_row)) # column根据文件格式修改
    elif flag == 'PDA_max':
        for filename in filenames:
            alldata[filename] = _zip_data(_read_PDA_max_data(path, filename, skip_row))
    else:
        return None
    
    return alldata

if __name__ == "__main__":
    pass

    # path = Path('/Users/zhouchen/Documents/CS_project/Surfactant_Compare')
    # a = read_all_data(path)
    # print(a['test.csv'][1])