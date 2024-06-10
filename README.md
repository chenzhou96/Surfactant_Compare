# Surfactant_Compare

## 版本
### **onlyPDA**
*本版本只用于PDA数据*<br>
*本版本加工原始数据后，不计算相似度，直接用谱图的y轴信息进行PCA分析*

<br>

## 简介
主程序为run.py，其余均为功能模块。实现功能为读取一个文件夹下的所有csv文件，对全部样品的谱图数据进行PCA分析
### 输入
变量|数据类型|描述
-|-|-
|**PATH**|*str*|指定文件夹的路径
**FLAG**|*str*|选择波谱数据格式，只有**PDA_max**, **PDA_single**两种格式可选
**COLUMN_INDEX**|*int*|文件中有效数据所在列
**SKIP_ROW**|*int*|文件中需要跳过的数据开头行数
**X_LEFT**, **RIGHT**|*float*|需要进行对比的x轴范围
**X_LABEL**, **X_GAP**|*float*|在x轴以X_LABEL为中心 左右宽度X_GAP的范围内寻找峰值位置作为基准点

*\* X_LABEL和X_GAP选出的区间要在X_LEFT和X_RIGHT的区间内*

### 输出
1. 输出为**一个csv文件**和命令行显示的提示信息
2. 输出的csv文件保存在PATH路径中
3. 输出的csv文件均以output开头，遇到文件名称重复时会在文件名加数字后缀

### 需要的python库
numpy  
pandas  
sklearn