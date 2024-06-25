# pylint: disable=W0718
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
import ssl

import contextlib
import aiohttp
import certifi

import octobot_commons.logging
import octobot_commons.constants


async def download_stream_file(
    output_file,
    file_url,
    aiohttp_session,
    data_chunk_size=5 * 2**20,
    is_aiofiles_output_file=False,
) -> str:
    """
    Download a big file with an aiohttp session
    :param output_file: the output file
    :param file_url: the file to be downloaded url
    :param aiohttp_session: the aiohttp session
    :param data_chunk_size: default value is 5*2**20 (5MB)
    :param is_aiofiles_output_file: When True, output_file.write will be awaited (when it's an aiofiles instance)
    :return downloaded file last_modified if given as response header
    """
    last_modified = None
    async with aiohttp_session.get(file_url) as resp:
        if resp.status != 200:
            try:
                text = await resp.text()
            except BaseException as err:
                text = f"error when reading resp text: {err}"
            raise RuntimeError(
                f"Failed to download file at url : {file_url} (status: {resp.status}, text: {text})"
            )
        while True:
            last_modified = resp.headers.get("Last-Modified", "unknown")
            chunk = await resp.content.read(data_chunk_size)
            if not chunk:
                # resp.content.read returns an empty chunk when completed
                break
            if is_aiofiles_output_file:
                await output_file.write(chunk)
            else:
                output_file.write(chunk)
    return last_modified


async def _check_local_certificates_availability(
    session: aiohttp.ClientSession, test_url: str
):
    try:
        # try fetching https://tentacles.octobot.online/ using local certificates
        async with session.get(test_url) as resp:
            if resp.status >= 400:
                octobot_commons.logging.get_logger(__name__).error(
                    f"Error when checking ssl certificates: fetching {test_url} returned {resp.status}. "
                    f"Considering certificates as valid."
                )
            return True
    except aiohttp.ClientConnectorCertificateError:
        return False
    except Exception as err:
        octobot_commons.logging.get_logger(__name__).info(
            f"Impossible to check ssl certificate: {err}. Consider valid"
        )
        return True


def _get_certify_aiohttp_client_session() -> aiohttp.ClientSession:
    # from https://docs.aiohttp.org/en/stable/client_advanced.html#example-use-certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))


async def get_ssl_fallback_aiohttp_client_session(
    test_url: str,
) -> aiohttp.ClientSession:
    """
    :return: an aiohttp.ClientSession using certifi ssl certificates if necessary
    """
    base_session = aiohttp.ClientSession()
    if (
        not octobot_commons.constants.ENABLE_CERTIFI_SSL_CERTIFICATES
        or await _check_local_certificates_availability(base_session, test_url)
    ):
        return base_session
    try:
        await base_session.close()
    except Exception as err:
        octobot_commons.logging.get_logger(__name__).exception(
            err, True, f"Error when closing test session: {err}"
        )
    # use custom SSL certificates session
    fallback_session = _get_certify_aiohttp_client_session()
    octobot_commons.logging.get_logger(__name__).info(
        "Falling back to certifi configured aiohttp connector."
    )
    return fallback_session


@contextlib.asynccontextmanager
async def ssl_fallback_aiohttp_client_session(test_url: str):
    """
    yields an aiohttp.ClientSession using certifi ssl certificates if necessary
    """
    session = None
    try:
        session = await get_ssl_fallback_aiohttp_client_session(test_url)
        yield session
    finally:
        if session is not None:
            await session.close()


@contextlib.asynccontextmanager
async def certify_aiohttp_client_session():
    """
    yields an aiohttp.ClientSession always using certifi ssl certificates
    """
    session = None
    try:
        octobot_commons.logging.get_logger(__name__).debug(
            "Using certifi configured aiohttp connector."
        )
        session = _get_certify_aiohttp_client_session()
        yield session
    finally:
        if session is not None:
            await session.close()
