import numpy as np

def _normalize_data(data: np.ndarray) -> np.ndarray:
    """
    返回z_score归一化 校正基线后的单个数据
    """

    z_score_data =  (data - data.mean()) / data.std()
    _ = z_score_data * (z_score_data < 0)
    under_zero = _.ravel()[np.flatnonzero(_)] # 提取所有小于0的数
    baseline = np.median(under_zero) # 取中位数？平均数？
    data = z_score_data + baseline
    data[data < 0] = 0

    return data

def _similarity_calculation(data1: np.ndarray, data2: np.ndarray) -> float:
    """
    输入一组数据 返回比较后的相似度
    """

    if len(data1) != len(data2):
        return None

    similar_level = 0
    total = data1.sum() + data2.sum()
    for index in range(len(data1)):
        denominator = max(data1[index], data2[index])
        if denominator:
            similar_level += (data1[index] + data2[index]) * (1- abs((data1[index] - data2[index]) / denominator))
        # 上述公式需要考虑除数为0
    
    return similar_level / total

def _similarity_calculation_No2(data1: np.ndarray, data2: np.ndarray) -> float:
    """
    输入一组数据 返回比较后的相似度
    """

    if len(data1) != len(data2):
        return None
    
    similar_level = 0
    total = 0
    for index in range(len(data1)):
        maxdata = max(abs(data1[index]), abs(data2[index]))
        total += maxdata
        similar_level += (maxdata - abs(data1[index] - data2[index]))
    
    return similar_level / total

def pairwise_comparsion(data_dict: dict) -> dict:
    """
    将文件夹内的所有数据进行两两比较 返回比较结果list
    """

    names = list(data_dict.keys())
    names.sort()
    results = dict()
    names_done = list()

    for name1 in names[:]:
        names_done.append(name1)
        for name2 in names[:]:
            if name2 not in names_done:
                results[f'{name1},{name2}'] = _similarity_calculation(_normalize_data(data_dict[name1]), _normalize_data(data_dict[name2]))
    
    return results

if __name__ == '__main__':
    pass
