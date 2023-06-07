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


async def download_stream_file(
    output_file,
    file_url,
    aiohttp_session,
    data_chunk_size=5 * 2**20,
    is_aiofiles_output_file=False,
):
    """
    Download a big file with an aiohttp session
    :param output_file: the output file
    :param file_url: the file to be downloaded url
    :param aiohttp_session: the aiohttp session
    :param data_chunk_size: default value is 5*2**20 (5MB)
    :param is_aiofiles_output_file: When True, output_file.write will be awaited (when it's an aiofiles instance)
    """
    async with aiohttp_session.get(file_url) as resp:
        if resp.status != 200:
            raise RuntimeError(
                f"Failed to download file at url : {file_url} (status: {resp.status})"
            )
        while True:
            chunk = await resp.content.read(data_chunk_size)
            if not chunk:
                # resp.content.read returns an empty chunk when completed
                break
            if is_aiofiles_output_file:
                await output_file.write(chunk)
            else:
                output_file.write(chunk)
