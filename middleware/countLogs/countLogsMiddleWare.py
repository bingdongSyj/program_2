#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 23:15
# @Author  : Liquid
# @Site    : 
# @File    : countLogsMiddleWare.py
# @Software: PyCharm
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

import logging

from middleware.prohibitCrawl.prohibitCrawlMiddleWare import get_real_ip


def yield_log(request):
    logger = logging.getLogger('my')
    logger.debug('{}\t{}\t{}\t{}'.format(get_real_ip(request), request.method, request.get_full_path(),
                                        request.META['SERVER_PROTOCOL']))


class CountLogsMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        yield_log(request)

    def process_response(self, request, response):
        pass
        return response

