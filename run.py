import csv
import PCA
from pathlib import Path
import data_loading as dl

# 参数设置
##注意事项：
##1. 文件为csv格式 数据间隔符号为英文逗号(,) 数据第一列必须代表谱图x轴
PATH = "D:\\Computer_Science\\Surfactant_Compare\\Test_T20_csv"
# PATH读取指定的文件夹位置 windows系统下需要使用\\代替路径中的\
FLAG = 'nmr'
# FLAG单引号内可选内容为 PDA_max, PDA_single, nmr 分别对应PDA最大值光谱,PDA单波长光谱,核磁谱图
SKIP_ROW = 0
# SKIP_ROW表示需要跳过的数据开头行数
COLUMN_INDEX = 2
# 当FLAG内容为PDA_single或nmr时 COLUMN_INDEX需要调整到数据所在列 比如数据在第二列则COLUMN_INDEX = 2
X_LEFT = 4.6
X_RIGHT = -0.5
# X_LEFT和X_RIGHT框选出谱图需要进行对比的x轴范围
X_LABEL = 0
X_GAP = 0.1
# X_LABEL用于作为基准点对齐谱图 比如nmr数据中选择化学位移为0的TMS峰 液相色谱数据中选择溶剂峰/倒峰的出峰时间
# PDA数据暂不需要设置这两个参数！！！
# 程序会在x轴以X_LABEL为中心 左右宽度X_GAP的范围内寻找峰值位置作为基准点
'''注意! X_LABEL和X_GAP选出的区间要在X_LEFT和X_RIGHT的区间内'''
# 设置结束

def _output_name(path: Path, data_name: str) -> Path:
    """
    输入路径和名称 返回合适的不重复csv名称
    """

    count = 0
    data_path = path / f'{data_name}.csv'
    while data_path.is_file():
        count += 1
        data_path = path / f'{data_name}_{count}.csv'

    return data_path

def _range_judgment() -> None:
    """
    判断x轴相关参数设置是否正确
    """

    if X_LEFT > X_RIGHT:
        x_max, x_min = X_LEFT, X_RIGHT
    else:
        x_max, x_min = X_RIGHT, X_LEFT

    if X_LABEL - X_GAP < x_min or X_LABEL + X_GAP > x_max:
        print("**********\nX轴相关参数设置错误\n**********")
        exit()

if __name__ == '__main__':
    
    '''
    ******Time consumption statistics******
    from pyinstrument import Profiler
    profiler = Profiler()
    profiler.start()
    ******Time consumption statistics******
    '''

    _range_judgment()
    path = Path(PATH)

    origin_data = dl.read_all_data(path, FLAG,
                                   column_index=COLUMN_INDEX,
                                   skip_row=SKIP_ROW,
                                   x_left = X_LEFT,
                                   x_right = X_RIGHT,
                                   x_label = X_LABEL,
                                   x_gap = X_GAP
                                   )

    '''
    # 用于数据origin_data进行人工检查
    for key, value in origin_data.items():
        output_path = path / f'output_{key}.csv'
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for item in value:
                writer.writerow([item])
    exit()
    '''

    pca_data = PCA.PCA_analysis(origin_data)
    if pca_data:
        pca_data_path = _output_name(path, 'output_pca_data')
        with open(pca_data_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filename', 'PCA_x', 'PCA_y'])
            for sample_name, single_pca_data in zip(*pca_data):
                writer.writerow([sample_name, *single_pca_data])
        
        print(f'**********\nPCA分析完成!\n数据保存在{pca_data_path}\n**********')
    else:
        print("**********\nPCA分析失败!\n**********")
        exit()
    
    '''
    ******Time consumption statistics******
    profiler.stop()
    profiler.print()
    ******Time consumption statistics******
    '''