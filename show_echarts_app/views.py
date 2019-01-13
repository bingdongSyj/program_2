from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

import pyecharts
# Create your views here.
from baizhi_web.settings import TABLE_PATH


def get_echarts(request):
    pie, pie_style = get_pie()
    result_list = get_db_data()
    paint_pie(result_list, pie, pie_style)
    return redirect('show_echarts_app:show_table')


def show_echarts_table(request):
    return render(request, template_name='table_pie.html')


def group_list(target_list):
    classify = []
    while len(target_list):
        flush = []
        next_one = target_list.pop(0)
        flush.append(next_one)
        for then in iter(target_list):
            if then[0] == next_one[0]:
                flush.append(then)
                target_list.remove(then)
        classify.append(flush)
    return classify


def get_cate(target_list):
    city = target_list[0][0]
    cate_list = []
    cate_num_list = []
    for k in target_list:
        cate_list.append(k[1])
        cate_num_list.append(k[2])
    return city, cate_list, cate_num_list


def get_pie():
    pie = pyecharts.Pie()
    style = pyecharts.Style()
    pie_style = style.add(
        label_pos="center",
        is_label_show=True,
        label_text_color=None
    )
    return pie, pie_style


def get_db_data():
    with connection.cursor() as cursor:
        cursor.execute("select city, category, count(category) from xpath_and_more group by cityid, category")
        # 返回tuple of tuple
        city_list = list(cursor.fetchall())  # (("zhj",18),(..),)
        result_list = group_list(city_list)
        result_list.append([('长沙', 'AI', 267), ('长沙', '大数据', 1572), ('长沙', '爬虫', 772)])
        result_list.append([('衡阳', 'AI', 67), ('衡阳', '大数据', 772)])
    return result_list


def paint_pie(result_list, pie, pie_style, hang=30):
    for num, classify in enumerate(result_list):
        city, cate_list, cate_num_list = get_cate(classify)
        if not num % 3 and num != 0:
            hang += 40
        pie.add(
            city, cate_list, cate_num_list, center=[20 + (num % 3) * 30, hang], radius=[30, 38], **pie_style
        )

    pie.render(TABLE_PATH + '\\table_pie.html')
