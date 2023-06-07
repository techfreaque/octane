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
import aiofiles
import os
import os.path as path
import shutil

import octobot_tentacles_manager.constants as constants


async def find_or_create(path_to_create, is_directory=True, file_content=""):
    if not path.exists(path_to_create):
        if is_directory:
            if not path.isdir(path_to_create):
                os.makedirs(path_to_create)
        else:
            if not path.isfile(path_to_create):
                # should be used for python init.py files only
                async with aiofiles.open(path_to_create, "w+") as file:
                    await file.write(file_content)
        return True
    return False


async def replace_with_remove_or_rename(new_file_or_dir_entry, dest_file_or_dir):
    try:
        if path.isfile(dest_file_or_dir):
            os.remove(dest_file_or_dir)
        else:
            if path.exists(dest_file_or_dir):
                shutil.rmtree(dest_file_or_dir)
    except PermissionError:
        # can't remove file / folder: might be locked (ex: .pyd files)
        # move it into TO_REMOVE_FOLDER for it to be deleted afterwards
        dest_path, dest_file = path.split(dest_file_or_dir)
        to_rm_folder = path.join(dest_path, constants.TO_REMOVE_FOLDER)
        await find_or_create(to_rm_folder, is_directory=True)
        shutil.move(dest_file_or_dir, path.join(to_rm_folder, dest_file))
    if path.isfile(new_file_or_dir_entry):
        shutil.copyfile(new_file_or_dir_entry, dest_file_or_dir)
    else:
        shutil.copytree(new_file_or_dir_entry, dest_file_or_dir)


def merge_folders(to_merge_folder, dest_folder, ignore_func=None):
    dest_folder_elements = {
        element.name: element for element in os.scandir(dest_folder)
    }
    elements = list(os.scandir(to_merge_folder))
    ignored_elements = ignore_func(to_merge_folder, (e.name for e in elements)) if ignore_func is not None else []
    filtered_elements = [element
                         for element in elements
                         if element.name not in ignored_elements]
    for element in filtered_elements:
        dest = path.join(dest_folder, element.name)
        if element.is_file():
            shutil.copy(element.path, dest)
        else:
            if element.name not in dest_folder_elements:
                shutil.copytree(element.path, dest, ignore=ignore_func if ignore_func is not None else None)
            else:
                merge_folders(element.path, dest_folder_elements[element.name].path, ignore_func=ignore_func)
