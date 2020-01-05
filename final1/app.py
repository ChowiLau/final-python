import pandas as pd
from flask import Flask
from flask import render_template, request, redirect
from pyecharts.charts import EffectScatter, Bar, Line, WordCloud, Map, Grid, Pie
from pyecharts.charts import Scatter
import numpy as np
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType, ThemeType
from pyecharts.charts import Bar, Tab, Line, Map, Timeline
from pyecharts.faker import Faker

app = Flask(__name__)


@app.route('/')
def index_bar():
    df = pd.read_csv("./static/data/GDP.csv")
    tl = Timeline()
    for i in range(2013, 2019):
        pie = (
            Pie()
                .add(
                "数值",
                list(zip(list(df.地区), list(df["{}年".format(i)]))),
                rosetype="radius",
                radius=["30%", "55%"],
            )
                .set_global_opts(title_opts=opts.TitleOpts())
        )
        tl.add(pie, "{}年".format(i))
    return render_template('index.html',
                           myechart=tl.render_embed(),
                           text=''' 从上面的模型中，我们可以看出近五年来，东南沿海地区的GDP生产总值在国内是较高的
                            以2018年为例，广东，浙江，山东三地的数值都要超过了80000。而西北地区的数值是偏低的
                            以2018年为例，西藏，青海，宁夏三地的数值都要低于10000''')


@app.route('/gdp_map')
def index_bar_every_1_tp():
    df = pd.read_csv("./static/data/GDP.csv")
    tl = Timeline()
    for i in range(2013, 2019):
        map0 = (
            Map()
                .add(
                "GDP生产值（单位：万亿）", list(zip(list(df.地区), list(df["{}年".format(i)]))), "china", is_map_symbol_show=False
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}各省份GDP总值".format(i), subtitle="",
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=18,
                                                                                     font_style="italic")),
                visualmap_opts=opts.VisualMapOpts(min_=1000, max_=80000),

            )
        )
        tl.add(map0, "{}年".format(i))
    return render_template('index.html',
                           myechart=tl.render_embed(),
                           text='''
                           从上面的模型中，我们可以看出近五年来，东南沿海地区的GDP生产总值在国内是较高的
                            以2018年为例，广东，浙江，山东三地的数值都要超过了80000。而西北地区的数值是偏低的
                            以2018年为例，西藏，青海，宁夏三地的数值都要低于10000
                           ''')


@app.route('/marry_line')
def index_bar_every():
    df = pd.read_csv("./static/data/marry.csv")
    r = (
        Line()
            .add_xaxis(list(df.columns))
            .add_yaxis("广东", list(df.loc[18]))
            .add_yaxis("浙江", list(df.loc[10]))
            .add_yaxis("山东", list(df.loc[14]))
            .add_yaxis("宁夏", list(df.loc[29]))
            .add_yaxis("西藏", list(df.loc[25]))
            .add_yaxis("青海", list(df.loc[28]))

            .set_global_opts(title_opts=opts.TitleOpts(title="结婚率（单位：%）"))
    )
    return render_template('index.html',
                           myechart=r.render_embed(),
                           text='''
                           从上面图的走势，我们可以看出，经济发达的三地，广东，浙江，山东的结婚率一年比一年降低，而经济欠发达的三地，宁夏，西藏，青海的结婚率却在逐年升高，甚至都超过了发达地区的结婚率水平。由此得出，经济发展水平可能会影响结婚率的水平，但随着时间的变迁，已经不再是影响结婚率水平的主因。
                           ''')


@app.route('/study_geo')
def index_bar_every_4():
    prevention = request.args.get("city")

    df = pd.read_csv(r'./static/data/study.csv')
    a = (
        Map()
            .add("学历水平（万人）", list(zip(list(df.地区), list(df[prevention]))))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=3500, min_=50),
            title_opts=opts.TitleOpts(title="6岁及以上女子大专学历人数{}年".format(prevention)),
        )
    )
    return render_template('index.html',
                           myechart=a.render_embed(),
                           text='''
                          ''', text1='''''')


# @app.route('/study_geo2')
# def index_bar_every_1():
#     df = pd.read_csv(r'./static/data/study.csv')
#     a = (
#         Map()
#             .add("学历水平（万人）", list(zip(list(df.地区), list(df['2018']))))
#             .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
#             .set_global_opts(
#             visualmap_opts=opts.VisualMapOpts(max_=3500, min_=50),
#             title_opts=opts.TitleOpts(title="6岁及以上女子大专学历人数2018年"),
#         )
#     )
#     return render_template('index.html',
#                            myechart=a.render_embed(),
#                            text=''' ''', text1=''' ''')


@app.route('/women_work')
def index_bar_every_2():
    df = pd.read_csv(r'./static/data/women work.csv')
    r = (
        Line()
            .add_xaxis(list(df.columns))
            .add_yaxis("全国", list(df.loc[0]))
            .set_global_opts(title_opts=opts.TitleOpts(title="工作率（单位：%）"))
    )
    return render_template('index.html',
                           myechart=r.render_embed(),
                           text='''由上面看可以看出，我国的女子受教育程度，以及女子的工作率每年都在上涨，呈现一个上涨的趋势。说明过往因为女子学历低，无法依靠自己的能力养活自己的情况正在逐渐减少，众多女性开始自力更生，有能力不依靠男性而是自己工作来养活自己
                                                    ''', text1='''通过找了我国各省的GDP数据，结婚率数据，女子学历水平数据，女子工作率水平这几个数据，多维度的对当前我国结婚率逐年下降的情况进行了分析思考，得出一下结论：
                            1.结婚率下降与不同地区经济水平发展并无太大关系
                            2.结婚率下降与女子学历水平和女子工作率有着正相关，越来越多的女性通过自己的能力可以不再依靠家庭而存货，更加追求自己的独立，也是导致结婚率下降的原因。''')


if __name__ == '__main__':
    app.run(debug=True)
