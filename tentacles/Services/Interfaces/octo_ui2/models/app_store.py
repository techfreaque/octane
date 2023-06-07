import octobot_tentacles_manager.loaders as loaders


def get_installed_tentacles_modules_dict() -> dict:
    return {
        _tentacle.name: {
            "name": _tentacle.name,
            "in_dev_mode": _tentacle.in_dev_mode,
            "ARTIFACT_NAME": _tentacle.ARTIFACT_NAME,
            "metadata": _tentacle.metadata,
            "origin_package": _tentacle.origin_package,
            "origin_repository": _tentacle.origin_repository,
            "tentacle_class_names": _tentacle.tentacle_class_names,
            "tentacle_group": _tentacle.tentacle_group,
            "tentacle_module_path": _tentacle.tentacle_module_path,
            "tentacle_path": _tentacle.tentacle_path,
            "tentacle_root_path": _tentacle.tentacle_root_path,
            "tentacle_root_type": _tentacle.tentacle_root_type,
            # "tentacle_type": _tentacle.tentacle_type,
            "tentacles_requirements": _tentacle.tentacles_requirements,
            "version": _tentacle.version,
        }
        for _tentacle in loaders.get_tentacle_classes().values()
    }
