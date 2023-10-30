# Surfactant_Compare

## 简介
主程序为run.py，其余均为功能模块。实现功能为读取一个文件夹下的所有csv文件，计算每个csv文件中谱图数据和其他csv文件谱图数据的相似度，并根据相似度对全部样品的谱图数据进行PCA分析
### 输入
1. run.py中需要输入的变量为PATH, FLAG, COLUMN_INDEX, SKIP_ROW
2. PATH: str 指定文件夹的路径
3. FLAG: str 选择波谱数据格式，只有‘PDA_max’, ‘PDA_single’, ‘nmr’三种格式可选
4. COLUMN_INDEX: int 文件中有效数据所在列
5. SKIP_ROW: int 文件中需要跳过的数据开头行数

### 输出
1. 输出为两个csv文件和命令行显示的提示信息
2. 输出的csv文件保存在PATH路径中
3. 输出的csv文件均以output开头，遇到文件名称重复时会在文件名加数字后缀

### 需要的python库
numpy  
pandas  
sklearn