import csv
from pathlib import Path
import pyecharts.options as opts
from pyecharts.charts import Scatter
from pyecharts.commons.utils import JsCode

# 参数设置
PATH = 'C:\\Users\\06427\\Desktop\\LC-pca_data.csv'
TITLE = '吐温80亲疏水性分布图'
# 设置结束

def _read_pca_data(path: str) -> list:
    """
    读取PCA分析后数据 用于绘图
    """

    with open(path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        csv_data = [row for row in csv_reader]

    return csv_data

def _plot(csv_data: list, scatter_path: str) -> bool:
    """
    画出PCA分析散点图
    """

    title = csv_data[0][2:]
    surfactant_data = csv_data[1:]
    x_data = [row[1] for row in surfactant_data]
    for index in range(len(surfactant_data)):
        surfactant_data[index] = surfactant_data[index][2:]
        # 注意此处surfactant_data丢掉了前两列
    y_data = surfactant_data
    
    (
        Scatter()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="",
            y_axis=y_data,
            symbol_size=20,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_series_opts()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(formatter=JsCode("function (params) {return params.value[2] + ' : ' + params.value[3];}"),
            ),
            title_opts = opts.TitleOpts(title=TITLE),
            legend_opts = opts.LegendOpts(is_show=False),
            datazoom_opts = opts.DataZoomOpts(type_="inside", range_start=0, range_end=100)
        )
        .render(scatter_path)
    )

if __name__ == "__main__":

    path = Path(PATH)
    _plot(_read_pca_data(PATH), str(path.with_name('pca_scatter.html')))