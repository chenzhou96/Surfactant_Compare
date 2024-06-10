import pandas as pd
from sklearn import decomposition

def PCA_analysis(origin_data: dict, components = 2) -> list:
    """
    输入两两比较的数据 进行PCA分析并输出 未读取到数据则返回None
    """

    sample_names = list(origin_data.keys())
    if not sample_names:
        return None
    
    data = pd.DataFrame()
    for name in sample_names:
        data[name] = origin_data[name]
    data = data.T

    # 把全为0的列都删除
    all_zero_columns = data.apply(lambda x: all(x == 0))
    data = data.drop(data.columns[all_zero_columns], axis=1)

    pca = decomposition.PCA(n_components=components)
    pca.fit(data.values)
    pca_data = pca.transform(data.values)

    return [sample_names, pca_data]

if __name__ == '__main__':

    pass