#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
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

from django.views import View
from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Session

import time
import requests

VERSION = '1.0.0'
STARTT = time.time()
HATSPLOIT = 'http://127.0.0.1:8008'

def get_uptime():
    return time.time() - STARTT

def check_connected():
    try:
        requests.get(HATSPLOIT)
    except Exception:
        return False
    return True


class Handler(LoginRequiredMixin, View):
    template = 'handler.html'
    login_url = '/login'

    def get(self, request):
        return render(request, self.template, {
            'connected': check_connected(),
        })
        
class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login'

    def get(self, request):
        return render(request, self.template, {
            'connected': check_connected(),
            'uptime': get_uptime(),
            'version': VERSION
        })

class Control(LoginRequiredMixin, View):
    template = 'control.html'
    login_url = '/login/'

    def get(self, request):
        try:
            sessions = requests.get(f"{HATSPLOIT}/sessions?list=all").json()
        except Exception:
            sessions = dict()

        for session_id in sessions.keys():
            if not Session.objects.filter(session_id=session_id).exists():
                Session.objects.create(
                    session_id=session_id,
                    platform=sessions[session_id]['platform'],
                    type=sessions[session_id]['type'],
                    host=sessions[session_id]['host'],
                    port=sessions[session_id]['port']
                )

        for session in Session.objects.all():
            if str(session.session_id) not in sessions.keys():
                Session.objects.filter(session_id=session.session_id).delete()

        sessions = Session.objects.all()
        return render(request, self.template, {
            'connected': check_connected(),
            'sessions': sessions
        })


class Dashboard(LoginRequiredMixin, View):
    template = 'dashboard.html'
    login_url = '/login/'
    
    C = 0

    def get(self, request):
        platforms = []
        locations = []

        opened_sessions = 0

        try:
            sessions = requests.get(f"{HATSPLOIT}/sessions?list=all").json()
            opened_sessions = int(requests.get(f"{HATSPLOIT}/sessions?count=all").text)
        except Exception:
            sessions = dict()

        for session_id in sessions.keys():
            if not Session.objects.filter(session_id=session_id).exists():
                Session.objects.create(
                    session_id=session_id,
                    platform=sessions[session_id]['platform'],
                    type=sessions[session_id]['type'],
                    host=sessions[session_id]['host'],
                    port=sessions[session_id]['port'],
                    latitude=sessions[session_id]['latitude'],
                    longitude=sessions[session_id]['longitude']
                )

        for session in Session.objects.all():
            if str(session.session_id) not in sessions.keys():
                self.C += 1
                Session.objects.filter(session_id=session.session_id).delete()

        for session in Session.objects.all():
            platforms.append({'x': session.platform,
                              'value': int(
                                    requests.get(f"{HATSPLOIT}/sessions?count={session.platform}").text)
                            })
            locations.append({'lat': session.latitude,
                              'long': session.longitude, 'name': f'Session #{str(session.session_id)}'})

        platforms = [dict(t) for t in {tuple(d.items()) for d in platforms}]
        sessions = Session.objects.all()

        return render(request, self.template, {
            'connected': check_connected(),
            'sessions': sessions,
            'platforms': platforms,
            'opened_sessions': opened_sessions,
            'closed_sessions': self.C,
            'top_platforms': len(platforms),
            'top_locations': len(locations),
            'locations': locations
        })


class Login(View):
    template = 'login.html'
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})
