#  Drakkar-Software OctoBot-Interfaces
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import gc
import pytest

import octobot_services.util

# ensure that imports that might be conflicting are importable


def test_web_imports():
    import flask
    import flask_caching
    import flask_compress
    import flask_socketio
    import gevent
    import geventwebsocket
    import flask_login
    import wtforms
    import flask_wtf


def test_telegram_imports():
    import telegram
    import telethon


def test_openai_imports():
    import openai
    # calling isinstance on openai proxies raises OpenAIError if OPENAI_API_KEY is missing or if a lib (numpy or panda)
    # can't be imported
    with pytest.raises(openai.OpenAIError):
        for obj in gc.get_objects():
            isinstance(obj, str)
    octobot_services.util.patch_openai_proxies()
    # isinstance can now be called on proxies
    for obj in gc.get_objects():
        isinstance(obj, str)
