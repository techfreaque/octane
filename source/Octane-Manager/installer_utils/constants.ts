const octane_packages: { [key: string]: string[] } = {
    "OctoBot": [
        "requirements.txt",
        "dev-requirements.txt",
        "strategy_maker_requirements.txt",
    ],
    "OctoBot-Backtesting": ["requirements.txt", "dev-requirements.txt"],
    "OctoBot-Commons": ["requirements.txt", "dev-requirements.txt"],
    "OctoBot-evaluators": ["requirements.txt", "dev-requirements.txt"],
    "OctoBot-Services": ["requirements.txt", "dev-requirements.txt"],
    "OctoBot-Tentacles-Manager": ["requirements.txt", "dev-requirements.txt"],
    "OctoBot-Trading": ["requirements.txt", "dev-requirements.txt"],
    "Async-Channel": ["requirements.txt"],
};

export { octane_packages };