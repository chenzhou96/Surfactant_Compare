import numpy as np
import pandas as pd
from sklearn import decomposition

# 参数设置
PATH = "C:\\Users\\06427\\Desktop\\项目_试剂化学成分对比V1.0\\相似度算法\\Triton"
FILENAME = "output_data4.csv"

def _compute_number(counts: int) -> int:
    """
    输入总数 计算元素个数
    """

    number = 1

    while counts >= number:

        if counts == number:
            return number

        counts -= number
        number +=1

    return None

def PCA_analysis(data_path: str, components = 2) -> list:
    """
    输入两两比较的数据 进行PCA分析并输出 未读取到数据则返回None
    """

    origin_data = pd.DataFrame(pd.read_csv(data_path, sep=',', names=['Sample A','Sample B','Similarity']))
    sample_names = list(set(origin_data['Sample A']) | set(origin_data['Sample B']))
    sample_names.sort()
    item_number = len(sample_names)

    if not item_number:
        return None
    
    data = pd.DataFrame(np.ones((item_number, item_number)), columns=sample_names, index=sample_names)

    for index, row in origin_data.iterrows():
        # print('_______________________________test____________________________')
        sample_A = row['Sample A']
        sample_B = row['Sample B']
        data[sample_A][sample_B] = data[sample_B][sample_A] = row['Similarity']

    pca = decomposition.PCA(n_components=components)
    pca.fit(data.values)
    pca_data = pca.transform(data.values)

    return [sample_names, pca_data]

if __name__ == '__main__':

    pass