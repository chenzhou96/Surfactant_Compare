import csv
import numpy as np
from pathlib import Path
from scipy.sparse import csc_matrix, eye, diags
from scipy.sparse.linalg import spsolve

def WhittakerSmooth(x, w, lambda_, differences=1):
    X = np.matrix(x)
    m = X.size
    E = eye(m, format='csc')
    for i in range(differences):
        E = E[1:] - E[:-1]  # numpy.diff() does not work with sparse matrix. This is a workaround.
    W = diags(w, 0, shape=(m, m))
    A = csc_matrix(W + (lambda_ * E.T * E))
    B = csc_matrix(W * X.T)
    background = spsolve(A, B)
    return np.array(background)

def airPLS(x, lambda_=2, porder=1, itermax=15):
    m = x.shape[0]
    w = np.ones(m)
    for i in range(1, itermax + 1):
        z = WhittakerSmooth(x, w, lambda_, porder)
        d = x - z
        dssn = np.abs(d[d < 0].sum())
        if (dssn < 0.001 * (abs(x)).sum() or i == itermax):
            if (i == itermax): print('WARING max iteration reached!')
            break
        w[d >= 0] = 0  # d>0 means that this point is part of a peak峰值, so its weight is set to 0 in order to ignore it
        w[d < 0] = np.exp(i * np.abs(d[d < 0]) / dssn)
        w[0] = np.exp(i * (d[d < 0]).max() / dssn)
        w[-1] = w[0]
    return w

def AirPLS(data):
    for item in range(data.shape[0]):
        data[item]=data[item]-airPLS(data[item])
    return data

def _read_csv_data(path: Path, filename: str, column: int) -> np.ndarray:
    """
    读取csv文件内第row行的数据
    返回ndarray数组
    """
    column -= 1
    try:
        path = str(path / filename)
        return np.loadtxt(path, delimiter=',') # delimiter根据文件格式修改
    except:
        return None
    
if __name__ == '__main__':
    path = Path('/Users/zhouchen/Desktop')

    data = _read_csv_data(path, filename='test1.csv', column=2)
    newdata = AirPLS(data + 0.01)

    count = 0
    data_name = 'output_data'
    data_path = path / f'{data_name}.csv'
    while data_path.is_file():
        count += 1
        data_path = path / f'{data_name}{count}.csv'

    with open(data_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for result in newdata:
            writer.writerow(result)