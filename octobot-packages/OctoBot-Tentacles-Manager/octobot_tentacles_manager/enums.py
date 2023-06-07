#  Drakkar-Software OctoBot-Tentacles-Manager
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

import enum


class ArtifactTypes(enum.Enum):
    TENTACLE = "tentacle"
    PROFILE = "profile"
    TENTACLE_PACKAGE = "tentacle_package"


class UploaderTypes(enum.Enum):
    S3 = "s3"
    NEXUS = "nexus"

class InstalledTentaclesModule(enum.Enum):
    NAME = "name"
    IN_DEV_MODE = "in_dev_mode"
    ARTIFACT_NAME = "artifact_name"
    METADATA = "metadata"
    ORIGIN_PACKAGE = "origin_package"
    ORIGIN_REPOSITORY = "origin_repository"
    TENTACLE_CLASS_NAMES = "tentacle_class_names"
    TENTACLE_GROUP = "tentacle_group"
    TENTACLE_MODULE_PATH = "tentacle_module_path"
    TENTACLE_PATH = "tentacle_path"
    TENTACLE_ROOT_PATH = "tentacle_root_path"
    TENTACLE_ROOT_TYPE = "tentacle_root_type"
    TENTACLES_REQUIREMENTS = "tentacles_requirements"
    VERSION = "version"
