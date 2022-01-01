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

import os
import sys
import argparse

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hatboard.core.settings')
    try:
        from django.core.management import call_command
        from django.core.wsgi import get_wsgi_application
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    description = "HatBoard is a HatSploit Framework web interface for executing attacks, handling and manipulating sessions and traffic."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--register', dest='register', action='store_true', help='Register a new user for HatBoard.')
    parser.add_argument('-a', '--address', dest='address', help='Run HatBoard on custom address.')
    args = parser.parse_args()

    application = get_wsgi_application()
    call_command('migrate')

    if args.register:
        call_command('createsuperuser')
        sys.exit(0)
    elif args.address:
        call_command('runserver', args.address)
        sys.exit(0)

    call_command('runserver', '0.0.0.0:7777')
