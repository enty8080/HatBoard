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

from django.db import models


class Session(models.Model):
    session_id = models.PositiveIntegerField()
    platform = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    port = models.PositiveIntegerField()
    latitude = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.session_id


class Payload(models.Model):
    number = models.PositiveIntegerField()
    category = models.CharField(max_length=250)
    payload = models.CharField(max_length=250)
    rank = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.number


class Module(models.Model):
    number = models.PositiveIntegerField()
    module = models.CharField(max_length=250)
    rank = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.number


class Option(models.Model):
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=250)
    required = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name
