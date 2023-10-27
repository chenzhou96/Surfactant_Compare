import csv
import PCA
from pathlib import Path
import data_loading as dl
import similarity_calculation as sc

if __name__ == '__main__':

# 参数设置
##注意事项：
##1. 文件为csv格式 数据间隔符号为,
    PATH = "C:\\Users\\06427\\Desktop\\项目_试剂化学成分对比V1.0\\相似度算法\\Triton"
    # PATH读取指定的文件夹位置 windows系统下需要使用\\代替路径中的\
    FLAG = 'PDA_single'
    # FLAG单引号内可选内容为 PDA_max, PDA_single, nmr 分别对应PDA最大值光谱,PDA单波长光谱,核磁谱图
    COLUMN_INDEX = 2 #固定不需要输入
    # 当FLAG内容为PDA_single或nmr时 COLUMN_INDEX需要调整到数据所在列 比如数据在第二列则COLUMN_INDEX = 2
    SKIP_ROW = 2 #固定不需要输入
    # 当FLAG内容为PDA_max时 SKIP_ROW表示需要跳过的数据开头行数
# 设置结束

def _output_name(path: Path, data_name: str) -> Path:
    """
    输入路径和名称 返回合适的不重复csv名称
    """

    count = 0
    data_path = path / f'{data_name}.csv'
    while data_path.is_file():
        count += 1
        data_path = path / f'{data_name}{count}.csv'

    return data_path

if __name__ == '__main__':
    
    path = Path(PATH)

    origin_data = dl.read_all_data(path, column_index=COLUMN_INDEX, skip_row=SKIP_ROW, flag=FLAG)
    if origin_data:
        results = sc.pairwise_comparsion(origin_data)
        compared_data_path = _output_name(path, 'output_compared_data')
        with open(compared_data_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # writer.writerow(['Sample A','Sample B','Similarity'])
            for key, result in results.items():
                sample_A, sample_B = key.split(',')
                writer.writerow([sample_A, sample_B, result])

        print(f'相似度分析完成!\n数据保存在{compared_data_path}\n')
    else:
        print("未读取到有效数据!\n")
        exit()

    pca_data = PCA.PCA_analysis(str(compared_data_path))
    if pca_data:
        pca_data_path = _output_name(path, 'output_pca_data')
        with open(pca_data_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filename', 'PCA_x', 'PCA_y'])
            for sample_name, signgle_pca_data in zip(*pca_data):
                writer.writerow([sample_name, *signgle_pca_data])
        
        print(f'PCA分析完成!\n数据保存在{pca_data_path}\n')

    else:
        print("PCA分析失败!\n")
        exit()