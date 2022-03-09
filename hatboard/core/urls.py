#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from django.contrib import admin
from django.urls import path
from hatboard.core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.Login.as_view(), name='login'),
    path('', views.Index.as_view(), name='index'),

    path('modules/', views.Modules.as_view(), name='modules'),
    path('payloads/', views.Payloads.as_view(), name='payloads'),
    path('attack/', views.Attack.as_view(), name='attack'),

    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('map/', views.Map.as_view(), name='map'),
    path('lookup/', views.Lookup.as_view(), name='lookup'),
    path('control/', views.Control.as_view(), name='control'),
    path('exchange/', views.Exchange.as_view(), name='exchange')
]
