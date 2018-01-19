#!/usr/bin/env python
# coding=utf-8
from django.http import HttpResponse

from TestModel.models import TestTable2

def testdb(request):
    test1 = TestTable2(name = 'marser2')
    test1.save()
    return HttpResponse("<p>数据添加成功</p>")
