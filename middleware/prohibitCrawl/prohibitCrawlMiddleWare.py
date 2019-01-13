#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 15:02
# @Author  : Liquid
# @Site    : 
# @File    : prohibitCrawl.py
# @Software: PyCharm
import time

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from baizhi_web.settings import MAX_VIEW_NUM, TIME_INTERVAL, EXP_TIME
from lib.redis_coon.redis_conn import conn

from toolsClass.prohibitRecorder import ProhibitRecorder


def get_real_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    return request.META['REMOTE_ADDR']


class ProhibitCrawlMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if 'prohibit_crawl' not in request.path and 'show_data' in request.path:
            ip = get_real_ip(request)
            if conn.get('prohibit_ip:'+ip):
                return HttpResponse('您访问的太频繁了，请休息会儿再来')
            recorder = ProhibitRecorder.get_all_key(ip)
            if not int(recorder['visit_num']) % MAX_VIEW_NUM:
                return redirect('back_end:show_pro_page')
            if recorder:
                # if int(recorder['visit_num']) % MAX_VIEW_NUM == 2:
                #     conn.setex('prohibit_ip:' + ip, '1', EXP_TIME)
                #     return HttpResponse('您访问的太频繁了，请休息会儿再来')
                if not int(recorder['visit_num']) % MAX_VIEW_NUM:
                    if time.time()-float(recorder['last_visit_time']) < TIME_INTERVAL:
                        conn.setex('prohibit_ip:'+ip, '1', EXP_TIME)
                        return HttpResponse('您访问的太频繁了，请休息会儿再来')
                    else:
                        ProhibitRecorder.update_last_visit_time(ip)
                    return redirect('back_end:show_pro_page')
                ProhibitRecorder.visit_num_increment(ip)
            else:
                ProhibitRecorder(ip)

    def process_response(self, request, response):
        # print(response)
        # print('---------------->', response.__dict__)
        print(response.content)
        return response
