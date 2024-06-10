import os, sys
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
    names_regex = re.compile(r'\.csv$')
    name_output = re.compile(r'^output')
    for name in filenames[:]:
        if not names_regex.search(name.lower()):
            filenames.remove(name)
        if name_output.search(name.lower()):
            filenames.remove(name)

    if filenames:
        return filenames
    else:
        print(f'**********\nNo csv file in {path}\n**********')
        exit()

def _read_csv_data(path: Path, filename: str, column_index: int, skip_row: int) -> np.ndarray:
    """
    读取csv文件内第row行的数据
    返回二维ndarray数组
    """
    column_index -= 1
    try:
        path = str(path / filename)
        return np.loadtxt(path, delimiter=',', skiprows=skip_row, usecols=(0, column_index)) # delimiter根据文件格式修改
    except Exception as error:
        print(f'**********\n{filename} read failed\nError: {error}\n**********')
        exit()
    
def _read_PDA_max_data(path: Path, filename: str, skip_row: int) -> np.ndarray:
    """
    读取PDA光谱文件
    返回二维ndarray数组
    """
    try:
        path = str(path / filename)
        data = np.loadtxt(path, delimiter=',', skiprows=skip_row) # delimiter根据文件格式修改
        # data为二维数组 第一列为时间 其他列为不同波段的吸光度
    except Exception as error:
        print(f'**********\n{filename} read failed\nError: {error}\n**********')
        exit()
    
    rows = data.shape[0]
    PDA_data = np.empty((rows, 2))
    PDA_data[:, 0] = data[:, 0]
    for index in range(rows):
        intensity = data[index][1:]
        PDA_data[index, 1] = intensity.max() # 有待和手动处理的数据对比验证一下

    return PDA_data

def _zip_data(csvdata: np.ndarray, n) -> np.ndarray:
    """
    压缩数据量
    返回横坐标数据点为n的新数据
    """

    rows = csvdata.shape[0]

    # 如果数据点不满n个 不需要进行压缩
    if n > rows:
        return csvdata

    zipdata = np.empty((n, 2))
    for step in range(n):
        start = int(step * rows / n)
        end = int((step + 1) * rows / n)
        zipdata[step, 0] = csvdata[start: end, 0].mean()
        zipdata[step, 1] = csvdata[start: end, 1].mean()

    return zipdata

def _select_x_axis(csvdata: np.ndarray, x_left: float, x_right: float) -> np.ndarray:
    """
    选择谱图的x轴范围
    返回二维ndarray数组
    """
    
    if x_left > x_right:
        x_max, x_min = x_left, x_right
    else:
        x_max, x_min = x_right, x_left

    row1 = csvdata[:, 0]
    row2 = csvdata[:, 1]
    bool_matrix = (row1 > x_min) & (row1 < x_max) # 选择合适x轴范围的布尔矩阵
    new_csvdata =  np.array([row1[bool_matrix], row2[bool_matrix]])

    return new_csvdata.T

    # new_csvdata = list()
    # for item in csvdata:
    #     if item[0] > x_min and item[0] < x_max:
    #         new_csvdata.append(item)
    
    # return np.array(new_csvdata)

def _find_datum(csvdata: np.ndarray, x_label, x_gap) -> int:
    """
    在给定的x轴范围内找峰 返回基准点距左右两端的距离
    """

    data = _select_x_axis(csvdata, x_label - x_gap, x_label + x_gap)

    dataRows = data.shape[0]
    csvdataRows = csvdata.shape[0]
    maxY = minY = data[0, 1]
    median = np.median(data[:, 1])

    for index in range(dataRows):
        if maxY < data[index, 1]:
            maxY = data[index, 1]
            maxX = data[index, 0]
        if minY > data[index, 1]:
            minY = data[index, 1]
            minX = data[index, 0]
    
    for index in range(csvdataRows):
        if maxX == csvdata[index, 0]:
            max_index = index
        if minX == csvdata[index, 0]:
            min_index = index
    
    if (maxY - median) > (median - minY):
        return [max_index, csvdataRows - max_index - 1]
    else:
        return [min_index, csvdataRows - min_index - 1]

def read_all_data(path: Path, flag: str, **args) -> dict:
    """
    读取路径文件夹内所有csv文件内容\n
    返回文件名和文件内容构成的字典\n
    **args\n
    column_index (int): read the target column in csv file\n
    skip_row (int): the number of ignored head rows in csv file\n
    x_left (float): select the range of x axis\n
    x_right (float): select the range of x axis\n
    x_label (float): select the datum point\n
    x_gap (float): select the deviation of datum point\n 
    """
    
    alldata = dict() # key为文件名称 value为谱图y轴数据
    datumData = dict()
    filenames = _read_filenames(path)

    data_point_number = 0
    minLeftDistance = minRightDistance = sys.maxsize

    if flag == 'nmr':
        for filename in filenames:
            read_data = _read_csv_data(path, filename, args['column_index'], args['skip_row'])
            selected_data = _select_x_axis(read_data, args['x_left'], args['x_right'])
            
            # 以第一个谱图的数据为基准 确定数据压缩量
            if not data_point_number:
                data_point_number = int((selected_data.shape[0]) / 10)
            zipped_data = _zip_data(selected_data, data_point_number)

            leftDistance, rightDistance = _find_datum(zipped_data, args['x_label'], args['x_gap'])
            if leftDistance < minLeftDistance:
                minLeftDistance = leftDistance
            if rightDistance < minRightDistance:
                minRightDistance = rightDistance
            alldata[filename] = zipped_data
            datumData[filename] = leftDistance

    elif flag == 'PDA_single':
        for filename in filenames:
            read_data = _read_csv_data(path, filename, args['column_index'], args['skip_row'])
            selected_data = _select_x_axis(read_data, args['x_left'], args['x_right'])

            # 以第一个谱图的数据为基准 确定数据压缩量
            if not data_point_number:
                data_point_number = int((selected_data.shape[0]) / 10)
            zipped_data = _zip_data(selected_data, data_point_number)

            alldata[filename] = zipped_data[:, 1]
        
        # 直接返回 暂不增加对齐步骤
        return alldata

    elif flag == 'PDA_max':
        for filename in filenames:
            read_data = _read_PDA_max_data(path, filename, args['skip_row'])
            selected_data = _select_x_axis(read_data, args['x_left'], args['x_right'])
            alldata[filename] = selected_data

            # 待完工 参考PDA_single

    else:
        print(f'**********\n{flag}格式不存在 请选择正确的FLAG参数\n**********')
        exit()

    wellBehavedData = dict()
    for key, value in alldata.items():
        datumIndex = datumData[key]
        wellBehavedData[key] = value[datumIndex - minLeftDistance:datumIndex + minRightDistance + 1, 1]

    # print([minLeftDistance, minRightDistance])    
    return wellBehavedData

if __name__ == "__main__":
    pass

    path = Path('C:\\Users\\06427\\Desktop\\Tween 80  原始数据CSV')
    filename = '1.csv'
    zip_data = _zip_data(_select_x_axis(_read_csv_data(path, filename, 2, 0), 6, -0.1), 1000)
    zip_data_path = path / 'select_data_zip1000.csv'
    import csv
    with open(zip_data_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in zip_data:
            writer.writerow(item)