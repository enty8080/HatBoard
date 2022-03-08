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

import time
import ipaddress
import requests

from .api import API

from .payloads import Payloads
from .models import Module
from .models import Session

from geopy.geocoders import Nominatim


class Utils:
    api = API()

    closed = 0
    version = '1.0.0'
    start = time.time()

    def get_uptime(self):
        return time.time() - self.start

    def check_connected(self):
        if self.api.request():
            return True
        return False

    def get_payloads(self):
        payloads = self.api.request('payloads', {
            'action': 'list'
        })
        
        if not payloads:
            payloads = dict()
        else:
            payloads = payloads.json()
            
        for number in payloads:
            if not Payload.objects.filter(number=number).exists():
                Payload.objects.create(
                    number=number,
                    category=payloads[payload]['Category'],
                    payload=payloads[payload]['Payload'],
                    rank=payloads[payload]['Rank'],
                    name=payloads[payload]['Name']
                )

        payloads = Payload.objects.all()
        return payloads

    def get_modules(self):
        modules = self.api.request('modules', {
            'action': 'list'
        })

        if not modules:
            modules = dict()
        else:
            modules = modules.json()

        for number in modules:
            if not Module.objects.filter(number=number).exists():
                Module.objects.create(
                    number=number,
                    module=modules[number]['Module'],
                    rank=modules[number]['Rank'],
                    name=modules[number]['Name'],
                    platform=modules[number]['Platform']
                )

        modules = Module.objects.all()
        return modules

    def get_sessions(self, locate=False):
        sessions = self.api.request('sessions', {
            'action': 'list'
        })

        if not sessions:
            sessions = dict()
        else:
            sessions = sessions.json()

        for session_id in sessions:
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
