import os
import random
import string
from urllib import parse

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from lib.captcha.image import ImageCaptcha
from middleware.prohibitCrawl.prohibitCrawlMiddleWare import get_real_ip
from show_data_app.models import DataInfo
from django.db import connection

from toolsClass.prohibitRecorder import ProhibitRecorder

PER_PAGE = 10


# select cityid, city from xpath_and_more group by cityid
def show_index(request):
    request.session['user'] = '1'
    # city_list = DataInfo.objects.values('cityid').annotate('city', 'cityid')
    with connection.cursor() as cursor:
        cursor.execute("select cityid, city from xpath_and_more group by cityid")
        # 返回tuple of tuple
        city_list = cursor.fetchall()  # (("zhj",18),(..),)

        print(city_list)
        print('---------------------')
        # print(cate_list)
        cate_list = []
        for city_id, city_name in city_list:
            cursor.execute("select distinct(category) from xpath_and_more where cityid=%s", [city_id])
            cate_list.append({city_id: cursor.fetchall()})
        print(cate_list)
    kwargs = {
        'city_list': city_list,
        'cate_list': cate_list,
    }
    return render(request, 'show_data_app/main.html', kwargs)


def show_introduce(request):
    return render(request, 'show_data_app/introduce.html')


def get_data(request, city_id, cate_name, page_num):
    data_list = DataInfo.objects.filter(cityid=city_id, category=cate_name).values('id', 'cityid', 'city',
                                                                                       'position', 'salary', 'company',
                                                                                       'company_type', 'working_exp',
                                                                                       'edu_level', 'company_website',
                                                                                       'emp_type')
    if not request.session.get('user'):
        data_list = data_list[:10]
    paginator = Paginator(object_list=data_list, per_page=PER_PAGE)
    data_count = len(data_list)
    if not page_num:
        page_num = 1
    page = paginator.page(page_num)
    return page, data_count


def show_menu(request):
    city_id = request.GET.get('city_id')
    cate_name = request.GET.get('cate_name')
    page_num = request.GET.get('page')
    if ' ' in cate_name:
        cate_name = parse.quote_plus(cate_name)
    page_obj, data_count = get_data(request, city_id, cate_name, page_num)
    kwargs = {
        'page': page_obj,
        'data_count': data_count,
        'city_id': city_id,
        'cate_name': cate_name
    }
    return render(request, 'show_data_app/menu.html', kwargs)


def exception_info():
    status_code = '400'
    data = '参数错误'
    return status_code, data


def is_login_deal(f):
    def func(*args, **kwargs):
        param = list(args)
        if not args[0].session.get('user'):
            param = list(args)
            param[1] = param[1][:10]
        return f(*tuple(param), **kwargs)
    return func


@is_login_deal
def deal_page(request, data_list, page_num, status_code='200'):
    try:
        paginator = Paginator(object_list=data_list, per_page=PER_PAGE)
        data_count = len(data_list)
        if not page_num:
            page_num = 1
        page = paginator.page(page_num)
        data = (page.object_list, data_count)
    except:

        status_code, data = exception_info()
    # print(status_code, page_num, '---------------------->')
    return status_code, data


def get_data_by_ajax(request, city_id, cate_name, city, cate, page_num):
    if not city and not cate:
        data_list = DataInfo.objects.filter(cityid=city_id, category=cate_name).values('id', 'cityid', 'city',
                                                                                       'position', 'salary', 'company',
                                                                                       'company_type', 'working_exp',
                                                                                       'edu_level', 'company_website',
                                                                                       'emp_type')
        status_code, data = deal_page(request, data_list, page_num)
    elif city and not cate:
        data_list = DataInfo.objects.filter(city=city).values('id', 'cityid', 'city', 'position', 'salary', 'company',
                                                              'company_type', 'working_exp', 'edu_level',
                                                              'company_website', 'emp_type')
        status_code, data = deal_page(request, data_list, page_num)
    elif not city and cate:
        data_list = DataInfo.objects.filter(category=cate).values('id', 'cityid', 'city', 'position', 'salary',
                                                                  'company', 'company_type', 'working_exp', 'edu_level',
                                                                  'company_website', 'emp_type')
        status_code, data = deal_page(request, data_list, page_num)
    else:
        status_code, data = exception_info()
    return status_code, data


def ajax_show_menu(request):
    city_id = request.GET.get('city_id')
    cate_name = request.GET.get('cate_name')
    page_num = request.GET.get('page')
    city = request.GET.get('city')
    cate = request.GET.get('cate')
    if not page_num.isdigit() or int(page_num) <= 0:
        return JsonResponse({'status': 400, 'data': '参数错误'})
    if ' ' in cate_name:
        cate_name = parse.quote_plus(cate_name)
    result = get_data_by_ajax(request, city_id, cate_name, city, cate, page_num)
    if result[0] == '200':
        page_obj, data_count = result[1]
        kwargs = {
            'city_id': city_id,
            'cate_name': cate_name,
            'page_obj': page_obj,
            'data_count': data_count,
            'page': page_num,
            'city': city,
            'cate': cate
        }
        print(kwargs, '---------------------->')
        return JsonResponse({'status': result[0], 'data': kwargs})
    return JsonResponse({'status': result[0], 'data': result[1]})


def show_prohibit_page(request):
    return render(request, 'prohibit_crawl.html')


def pro_crawl_captcha(request):
    image = ImageCaptcha(fonts=[os.path.abspath('lib/captcha/verdana.ttf')])
    code = random.sample(string.printable[:62], 5)
    code = ''.join(code)
    request.session['captcha'] = code
    data = image.generate(code)
    print(code)
    return HttpResponse(data, 'image/png')


def validate_pro_crawl_captcha(request):
    pro_crawl_code = request.GET.get('pro_crawl_code')
    if pro_crawl_code and len(pro_crawl_code) == 5:
        capt = request.session.get('captcha')
        if capt and pro_crawl_code.lower() == capt.lower():
            ip = get_real_ip(request)
            ProhibitRecorder.visit_num_increment(ip)
            return JsonResponse({'status': 200, 'data': ProhibitRecorder.get_target_url(ip)})
        return JsonResponse({'status': 400, 'data': '您输入的验证码不对'})
    return JsonResponse({'status': 400, 'data': '验证失败'})
