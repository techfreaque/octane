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
import flask
import os

import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Services.Interfaces.octo_ui2.models.octo_ui2 as octo_ui2_models



def _send_file(base_dir, file_path):
    base_path, file_name = os.path.split(file_path)
    return flask.send_from_directory(os.path.join(base_dir, base_path), file_name)


def register(blueprint):
    @octo_ui2_models.octane_route(blueprint, route="/tentacle_media", can_be_shared_public=True)
    def tentacle_media():
        return _tentacle_media()
        
    @octo_ui2_models.octane_route(blueprint, route="/tentacle_media/<path:path>", can_be_shared_public=True)
    def tentacle_media_with_path(path=None):
        return _tentacle_media(path=path)
        
    def _tentacle_media(path=None):
        # images
        if models.is_valid_tentacle_image_path(path):
            # reference point is the web interface directory: use OctoBot root folder as a reference
            return _send_file("../../../..", path)
    
    
    @octo_ui2_models.octane_route(blueprint, route="/profile_media/<path:path>", can_be_shared_public=True)
    def profile_media(path):
        # images
        if models.is_valid_profile_image_path(path):
            # reference point is the web interface directory: use OctoBot root folder as a reference
            return _send_file("../../../..", path)
    
    
    @octo_ui2_models.octane_route(blueprint, route="/exchange_logo/<name>", can_be_shared_public=True)
    def exchange_logo(name):
        return flask.jsonify(models.get_exchange_logo(name))
    
    
    @octo_ui2_models.octane_route(blueprint, route="/audio_media/<name>", can_be_shared_public=True)
    def audio_media(name):
        if models.is_valid_audio_path(name):
            # reference point is the web interface directory: use OctoBot root folder as a reference
            return _send_file("static/audio", name)
    
    
    @octo_ui2_models.octane_route(blueprint, route="/currency_logos", methods=['POST'], can_be_shared_public=True)
    def cryptocurrency_logos():
        request_data = flask.request.get_json()
        return flask.jsonify(models.get_currency_logo_urls(request_data["currency_ids"]))
