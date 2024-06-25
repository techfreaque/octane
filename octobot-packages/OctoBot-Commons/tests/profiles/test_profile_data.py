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
#  License along with this library.*
import copy

import pytest

import octobot_commons.profiles as profiles
import octobot_commons.profiles.profile_data as profile_data_import
import octobot_commons.constants as constants
import octobot_commons.enums as enums

from tests.profiles import get_profile_path, profile


@pytest.fixture
def profile_data_dict():
    return {
        'profile_details': {
            'name': 'profile_name 42',
            'id': 'default',
            'version': "42.42.1b",
            'bot_id': "1234-1224-0000"
        },
        'crypto_currencies': [
            {
                'trading_pairs': ['BTC/USDT'],
                'name': 'Bitcoin',
                'enabled': True
            },
            {
                'trading_pairs': ['ETH/USDT'],
                'name': 'ETH',
                'enabled': False
            }
        ], 'exchanges': [
            {
                'exchange_credential_id': '123-plop',
                'internal_name': 'cryptocom'
            }
        ], 'trader': {
            'enabled': True
        }, 'trader_simulator': {
            'enabled': False,
            'starting_portfolio': {
                'BTC': 10,
                'USDT': 1000
            },
            'maker_fees': 0.1,
            'taker_fees': 0.1
        }, 'trading': {
            'reference_market': 'BTC',
            'minimal_funds': [
                {
                    "asset": "BTC",
                    "available": 12,
                    "total": 12,
                },
                {
                    "asset": "PLOP",
                    "available": 0.1111,
                    "total": 0.2222,
                }
            ],
            'risk': 0.5
        }, 'tentacles': [
            {
                'name': 'plopEvaluator',
                'config': {},
            },
            {
                'name': 'plopEvaluator',
                'config': {
                    'a': True,
                    'other': {
                        'l': [1, 2],
                        'n': None,
                    }
                },
            },
        ], 'options': {
            'values': {
                'plop_key': 'hola senior'
            }
        }, 'backtesting_context': {
            'start_time_delta': 11313.22,
            'update_interval': 444,
            'starting_portfolio': {
                'plop_key': 'hola senior'
            },
            'exchanges': [
                'binance', 'kucoin'
            ]
        }
    }


@pytest.fixture
def min_profile_data_dict():
    return {
        'profile_details': {
            'name': 'min_profile',
        },
        'crypto_currencies': [
            {
                'trading_pairs': ['BTC/USDT'],
            },
            {
                'trading_pairs': ['ETH/USDT'],
                'enabled': False
            }
        ], 'trading': {
            'reference_market': 'BTC',
        }, 'tentacles': [
            {
                'name': 'plopEvaluator',
                'config': {},
            },
            {
                'name': 'plopEvaluator',
                'config': {
                    'a': True,
                    'other': {
                        'l': [1, 2],
                        'n': None,
                    }
                },
            },
        ],
        'backtesting_context': {
            'start_time_delta': 11313.22
        }, 'options': {
            'values': {
                'plop_key': 'hola !!!',
                'jour': 'nuit',
            }
        }
    }


def test_from_profile(profile):
    profile_data = profiles.ProfileData.from_profile(profile.read_config())
    # check one element per attribute to be sure it's all parsed
    assert profile_data.profile_details.name == "default"
    assert profile_data.crypto_currencies[0].trading_pairs == ['BTC/USDT']
    assert profile_data.exchanges == []
    assert profile_data.trader.enabled is False
    assert profile_data.trader_simulator.enabled is True
    assert profile_data.trader_simulator.starting_portfolio == {'BTC': 10, 'USDT': 1000}
    assert profile_data.trading.risk == 0.5
    assert profile_data.tentacles == []


def test_to_profile(profile):
    profile_data = profiles.ProfileData.from_profile(profile.read_config())
    created_profile = profile_data.to_profile("plop_path")
    # force missing values
    for crypto_data in profile.config[constants.CONFIG_CRYPTO_CURRENCIES].values():
        crypto_data[constants.CONFIG_ENABLED_OPTION] = crypto_data.get(constants.CONFIG_ENABLED_OPTION, True)
    # remove not stored values
    profile.config[constants.CONFIG_EXCHANGES] = {}
    profile.avatar = profile.description = ""
    profile.complexity = enums.ProfileComplexity.MEDIUM
    profile.risk = enums.ProfileRisk.MODERATE
    profile.profile_type = enums.ProfileType.LIVE
    profile.origin_url = None
    # if both parsing and transforming return the same profile as original one, the whole chain works
    profile_dict = profile.as_dict()
    assert profile_dict == created_profile.as_dict()


def test_from_dict(profile_data_dict):
    # use second MinimalFund syntax
    profile_data_dict = copy.deepcopy(profile_data_dict)
    profile_data_dict["trading"]['minimal_funds'].append(
        {
            "asset": "ETH",
            "value": 111.2,
        }
    )
    profile_data = profiles.ProfileData.from_dict(profile_data_dict)
    # check one element per attribute to be sure it's all parsed
    assert profile_data.profile_details.name == "profile_name 42"
    assert profile_data.crypto_currencies[0].trading_pairs == ['BTC/USDT']
    assert profile_data.exchanges[0].exchange_credential_id == "123-plop"
    assert profile_data.exchanges[0].internal_name == "cryptocom"
    assert profile_data.trader.enabled is True
    assert profile_data.trader_simulator.enabled is False
    assert profile_data.trader_simulator.starting_portfolio == {'BTC': 10, 'USDT': 1000}
    assert profile_data.trading.risk == 0.5
    assert profile_data.trading.minimal_funds == [
        profiles.MinimalFund("BTC", 12, 12),
        profiles.MinimalFund("PLOP", 0.1111, 0.2222),
        profiles.MinimalFund("ETH", 111.2, 111.2),
    ]
    assert profile_data.tentacles[0].name == "plopEvaluator"
    assert profile_data.tentacles[1].config["other"]["l"] == [1, 2]


def test_from_min_dict(min_profile_data_dict):
    profile_data = profiles.ProfileData.from_dict(min_profile_data_dict)
    # check one element per attribute to be sure it's all parsed
    assert profile_data.profile_details.name == "min_profile"
    assert profile_data.crypto_currencies[0].trading_pairs == ['BTC/USDT']
    assert profile_data.crypto_currencies[0].name is None
    assert profile_data.crypto_currencies[0].enabled is True
    assert profile_data.crypto_currencies[1].trading_pairs == ['ETH/USDT']
    assert profile_data.crypto_currencies[1].name is None
    assert profile_data.crypto_currencies[1].enabled is False
    assert profile_data.exchanges == []
    assert profile_data.trader.enabled is True
    assert profile_data.trader_simulator.enabled is False
    assert profile_data.trader_simulator.starting_portfolio == {}
    assert profile_data.trading.risk == 1
    assert profile_data.tentacles[0].name == "plopEvaluator"
    assert profile_data.tentacles[1].config["other"]["l"] == [1, 2]
    assert profile_data.options.values["jour"] == "nuit"
    assert profile_data.options.values["plop_key"] == "hola !!!"
    full_profile_data_dict = profile_data.to_dict(include_default_values=True)
    assert len(full_profile_data_dict) > len(min_profile_data_dict)
    profile_data_dict = profile_data.to_dict(include_default_values=False)
    # default values in values but: keys are present except for exchanges, which content is empty (default)
    full_profile_data_dict_keys_without_exchange = list(full_profile_data_dict.keys())
    full_profile_data_dict_keys_without_exchange.remove("exchanges")
    assert sorted(list(profile_data_dict.keys())) == sorted(full_profile_data_dict_keys_without_exchange)


def test_from_dict_objects(profile_data_dict):
    profile_data_objects = profiles.ProfileData.from_dict(profile_data_dict)
    profile_data = profiles.ProfileData.from_dict({
        "profile_details": profile_data_objects.profile_details,
        "crypto_currencies": profile_data_objects.crypto_currencies,
        "exchanges": profile_data_objects.exchanges,
        "trader": profile_data_objects.trader,
        "trader_simulator": profile_data_objects.trader_simulator,
        "trading": profile_data_objects.trading,
        "tentacles": profile_data_objects.tentacles,
        "options": profile_data_objects.options,
    })
    # check one element per attribute to be sure it's all parsed
    assert profile_data.profile_details.version == "42.42.1b"
    assert profile_data.crypto_currencies[0].trading_pairs == ['BTC/USDT']
    assert profile_data.exchanges[0].exchange_credential_id == "123-plop"
    assert profile_data.trader.enabled is True
    assert profile_data.trader_simulator.enabled is False
    assert profile_data.trader_simulator.starting_portfolio == {'BTC': 10, 'USDT': 1000}
    assert profile_data.trading.risk == 0.5
    assert profile_data.tentacles[0].name == "plopEvaluator"
    assert profile_data.tentacles[1].config["other"]["l"] == [1, 2]
    assert profile_data.options.values['plop_key'] == 'hola senior'
    assert profile_data.backtesting_context == profile_data_import.BacktestingContext()


def test_to_dict(profile_data_dict):
    profile_data = profiles.ProfileData.from_dict(profile_data_dict)
    # if both parsing and transforming return the same profile as original one, the whole chain works
    assert profile_data_dict == profile_data.to_dict()

    dict_without_default_values = profile_data.to_dict(include_default_values=False)
    assert profile_data_dict != dict_without_default_values

    # ensure no empty elements
    assert len(dict_without_default_values) == len(profile_data_dict)
    for values in dict_without_default_values.values():
        assert len(values)
