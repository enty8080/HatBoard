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

from .api import API
from .utils import Utils

from .models import Option

api = API()
utils = Utils()


class Attack(LoginRequiredMixin, View):
    template = 'attack.html'
    login_url = '/login/'

    def post(self, request):
        options = {}

        if 'module' in request.POST:
            module = request.POST['module']

            if module:
                api.request('modules', {
                    'action': 'use',
                    'module': module
                })

                options = api.request('modules', {
                    'action': 'options'
                })

                if not options:
                    options = dict()
                else:
                    options = options.json()

                for option in options:
                    if not Module.objects.filter(name=option).exists():
                        Option.objects.create(
                            name=option,
                            value=options[option]['Value'],
                            required=options[option]['Required'],
                            description=options[option]['Description']
                        )
                    else:
                        Module.objects.filter(name=option).delete()
                        Option.objects.create(
                            name=option,
                            value=options[option]['Value'],
                            required=options[option]['Required'],
                            description=options[option]['Description']
                        )

                options = Option.objects.all()

        return render(request, self.template, {
            'connected': utils.check_connected(),
            'modules': utils.get_modules(),
            'options': options
        })

    def get(self, request):
        return render(request, self.template, {
            'connected': utils.check_connected(),
            'modules': utils.get_modules(),
            'options': {}
        })


class Exchange(LoginRequiredMixin, View):
    template = 'exchange.html'
    login_url = '/login/'

    def post(self, request):
        if 'session' in request.POST:
            session = request.POST['session']

            if session:
                if 'local_file' not in request.POST:
                    remote_file = request.POST['remote_file']
                    local_path = request.POST['local_path']

                    if remote_file and local_path:
                        api.request('sessions', {
                            'action': 'download',
                            'session': session,
                            'remote_file': remote_file,
                            'local_path': local_path
                        })
                else:
                    local_file = request.POST['local_file']
                    remote_path = request.POST['remote_path']

                    if local_file and remote_path:
                        api.request('sessions', {
                            'action': 'upload',
                            'session': session,
                            'local_file': local_file,
                            'remote_path': remote_path
                        })

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
                    api.request('sessions', {
                        'action': 'close',
                        'session': session
                    })
                else:
                    command = request.POST['command']

                    if command:
                        output = api.request('sessions', {
                            'action': 'execute',
                            'session': session,
                            'command': command,
                            'output': 'yes'
                        }).text

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


class Modules(LoginRequiredMixin, View):
    template = 'modules.html'
    login_url = '/login/'

    def get(self, request):
        modules = utils.get_modules()

        categories = []
        platforms = []

        for module in modules:
            category = module.category
            amount = 0

            for current_module in modules:
                if current_module.category == category:
                    amount += 1

            category = [category.title(), amount]

            if category not in categories:
                categories.append(category)

            platform = module.platform
            amount = 0

            for current_module in modules:
                if current_module.platform == platform:
                    amount += 1

            if platform in ['apple_ios']:
                platform = 'Apple iOS'
            elif platform in ['macos']:
                platform = 'macOS'
            else:
                platform = platform.title()

            platform = [platform, amount]

            if platform not in platforms:
                platforms.append(platform)

        return render(request, self.template, {
            'connected': utils.check_connected(),
            'modules': modules,

            'categories': categories,
            'platforms': platforms
        })


class Payloads(LoginRequiredMixin, View):
    template = 'payloads.html'
    login_url = '/login/'

    def get(self, request):
        payloads = utils.get_payloads()

        categories = []
        platforms = []

        for payload in payloads:
            category = payload.category
            amount = 0

            for current_payload in payloads:
                if current_payload.category == category:
                    amount += 1

            category = [category.title(), amount]

            if category not in categories:
                categories.append(category)

            platform = payload.platform
            amount = 0

            for current_payload in payloads:
                if current_payload.platform == platform:
                    amount += 1

            if platform in ['apple_ios']:
                platform = 'Apple iOS'
            elif platform in ['macos']:
                platform = 'macOS'
            else:
                platform = platform.title()

            platform = [platform, amount]

            if platform not in platforms:
                platforms.append(platform)

        return render(request, self.template, {
            'connected': utils.check_connected(),
            'payloads': payloads,

            'categories': categories,
            'platforms': platforms
        })


class Dashboard(LoginRequiredMixin, View):
    template = 'dashboard.html'
    login_url = '/login/'

    def post(self, request):
        output = ""

        if 'session' in request.POST and 'command' in request.POST:
            session = request.POST['session']
            command = request.POST['command']

            output = api.request('sessions', {
                'action': 'execute',
                'session': session,
                'command': command,
                'output': 'yes'
            }).text

            output = '<pre>' + output.replace('"', '') + '</pre>'
            output = output.replace("\\n", '<br>')

        return HttpResponse(json.dumps({
            'output': output
        }))

    def get(self, request):
        platforms = []
        locations = []

        if utils.check_connected():
            opened_sessions = len(api.request('sessions', {
                'action': 'list'
            }).json)
        else:
            opened_sessions = 0

        sessions = utils.get_sessions(locate=True)

        for session in sessions:
            platform = session.platform[session.platform.find('; ')+2:]
            platform = [platform, len(api.request('sessions', {
                'action': 'list',
                'fetch': platform
            }).json)]

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
            token = api.login(username, password)
            api.api_token = token

            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})
