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

import json
import requests

from django.views import View
from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import Utils

utils = Utils()


class Attack(LoginRequiredMixin, View):
    template = 'attack.html'
    login_url = '/login/'

    def post(self, request):
        if 'session' in request.POST:
            session = request.POST['session']

            if session:
                if 'local_file' not in request.POST:
                    remote_file = request.POST['remote_file']
                    local_path = request.POST['local_path']

                    if remote_file and local_path:
                        requests.get(f"{utils.api}/sessions?download={remote_file}&path={local_path}&id={session}")
                else:
                    local_file = request.POST['local_file']
                    remote_path = request.POST['remote_path']

                    if local_file and remote_path:
                        request.get(f"{utils.api}/sessions?upload={local_file}&path={remote_path}&id={session}")

        return render(request, self.template, {
            'connected': utils.check_connected(),
            'sessions': utils.get_sessions()
        })

    def get(self, request):
        return render(request, self.template, {
            'connected': utils.check_connected(),
            'sessions': utils.get_sessions()
        })


class Lookup(LoginRequiredMixin, View):
    template = 'lookup.html'
    login_url = '/login/'

    def get(self, request):
        locations = []
        sessions = utils.get_sessions(locate=True)

        for session in sessions:
            location = [session.country, 0]
            if location not in locations:
                locations.append(location)

        for session in sessions:
            for i in range(0, len(locations)):
                if session.country == locations[i][0]:
                    locations[i][1] += 1

        return render(request, self.template, {
            'locations': locations,
            'sessions': sessions,
            'connected': utils.check_connected(),
        })


class Map(LoginRequiredMixin, View):
    template = 'map.html'
    login_url = '/login/'

    def get(self, request):
        locations = []
        sessions = utils.get_sessions(locate=True)

        for session in sessions:
            location = [session.country, 0]
            if location not in locations:
                locations.append(location)

        for session in sessions:
            for i in range(0, len(locations)):
                if session.country == locations[i][0]:
                    locations[i][1] += 1

        return render(request, self.template, {
            'locations': locations,
            'connected': utils.check_connected(),
        })


class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        return render(request, self.template, {
            'connected': utils.check_connected(),
            'uptime': utils.get_uptime(),
            'version': utils.version
        })


class Control(LoginRequiredMixin, View):
    template = 'control.html'
    login_url = '/login/'

    def post(self, request):
        output = ""

        if 'session' in request.POST:
            session = request.POST['session']

            if session:
                if 'command' not in request.POST:
                    requests.get(f"{utils.api}/sessions?close={session}")
                else:
                    command = request.POST['command']

                    if command:
                        output = requests.get(
                            f"{utils.api}/sessions?command={command}&output=yes&id={session}"
                        ).text

                        output = '<pre>' + output.replace('"', '') + '</pre>'
                        output = output.replace('\\n', '<br>')

        return render(request, self.template, {
            'connected': utils.check_connected(),
            'sessions': utils.get_sessions(),
            'output': output
        })

    def get(self, request):
        return render(request, self.template, {
            'connected': utils.check_connected(),
            'sessions': utils.get_sessions(),
            'output': ""
        })


class Dashboard(LoginRequiredMixin, View):
    template = 'dashboard.html'
    login_url = '/login/'

    def post(self, request):
        output = ""

        if 'session' in request.POST and 'command' in request.POST:
            session = request.POST['session']
            command = request.POST['command']

            output = requests.get(
                f"{utils.api}/sessions?command={command}&output=yes&id={session}"
            ).text

            output = '<pre>' + output.replace('"', '') + '</pre>'
            output = output.replace("\\n", '<br>')

        return HttpResponse(json.dumps({'output': output}))

    def get(self, request):
        platforms = []
        locations = []

        try:
            opened_sessions = int(requests.get(f"{utils.api}/sessions?count=all").text)
        except Exception:
            opened_sessions = 0

        sessions = utils.get_sessions(locate=True)

        for session in sessions:
            platform = session.platform[session.platform.find('; ')+2:]
            platform = [platform, int(
                requests.get(f"{utils.api}/sessions?count={platform.lower()}").text
            )]

            if platform not in platforms:
                platforms.append(platform)

            location = [session.country, 0]
            if location not in locations:
                locations.append(location)

        for session in sessions:
            for i in range(0, len(locations)):
                if session.country == locations[i][0]:
                    locations[i][1] += 1

        return render(request, self.template, {
            'connected': utils.check_connected(),
            'sessions': sessions,
            'platforms': platforms,

            'opened_sessions': opened_sessions,
            'closed_sessions': utils.closed,

            'top_platforms': len(platforms),
            'top_locations': len(locations),
            'locations': locations
        })


class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {
            'connected': utils.check_connected(),
            'form': form
        })

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
