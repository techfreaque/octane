# pylint: disable=C0116
#  Drakkar-Software OctoBot-Commons
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
import octobot_commons.enums


class Signal:
    def __init__(self, topic: str, content: dict, **_):
        self.topic: str = topic
        self.content: dict = content

    def to_dict(self) -> dict:
        return {
            octobot_commons.enums.SignalsAttrs.TOPIC.value: self.topic,
            octobot_commons.enums.SignalsAttrs.CONTENT.value: self.content,
        }

    def __str__(self):
        return f"{self.to_dict()}"
