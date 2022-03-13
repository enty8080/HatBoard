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

import requests

from .models import Account


class API:
    url = "http://{}:{}/"

    def login(self, username, password, host, port):
        request = self.url.format(host, str(port)) + 'login'

        try:
            response = requests.post(request, data={
                'username': username,
                'password': password
            })

            if response:
                token = response.json()['token']

                if not Account.objects.filter(token=token).exists():
                    Account.objects.create(
                        token=token,
                        host=host,
                        port=int(port)
                    )

                return True

        except Exception:
            pass

        return False

    def request(self, action='', data={}):
        accounts = Account.objects.all()

        if accounts:
            for account in accounts:
                data.update({
                    'token': account.token
                })

                request = self.url.format(account.host,
                                          str(account.port)) + action

                try:
                    response = requests.post(request, data=data)

                    if response.status_code == 401:
                        continue

                    return response

                except Exception:
                    continue

        return None
