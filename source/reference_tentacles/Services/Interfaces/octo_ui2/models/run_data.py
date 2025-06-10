import octobot_commons.databases as databases
import octobot_commons.enums as commons_enums
import octobot_services.interfaces.util as interfaces_util

import tentacles.Services.Interfaces.web_interface.models as models
import tentacles.Meta.Keywords.scripting_library.backtesting as backtesting


def get_backtesting_run_data(campaigns_to_load):
    trading_mode = models.get_config_activated_trading_mode()
    campaign_names, metadata = interfaces_util.run_in_bot_async_executor(
        backtesting.read_metadata(
            runs_to_load_settings=campaigns_to_load,
            trading_mode=trading_mode,
            include_optimizer_runs=True,
        )
    )
    return {"data": metadata, "campaigns": campaign_names}




def delete_run_data(trading_mode, run_data_identifiers):
    for run_data_identifier in run_data_identifiers:
        databases.RunDatabasesIdentifier(
            trading_mode,
            optimization_campaign_name=run_data_identifier["campaign_name"],
            backtesting_id=run_data_identifier["backtesting_id"],
            optimizer_id=run_data_identifier["optimizer_id"] or None,
        ).remove_all()
    interfaces_util.run_in_bot_async_executor(
        _update_backtesting_metadata(trading_mode, run_data_identifiers)
    )
    return {"title": f"{len(run_data_identifiers)} runs deleted"}


async def _update_backtesting_metadata(trading_mode, run_data_identifiers):
    backtesting_by_optimizer_by_campaign = {}
    for run_data_identifier in run_data_identifiers:
        campaign_name = run_data_identifier["campaign_name"]
        backtesting_id = run_data_identifier["backtesting_id"]
        optimizer_id = run_data_identifier["optimizer_id"] or None
        try:
            backtesting_by_optimizer_by_campaign[campaign_name][optimizer_id].add(
                backtesting_id
            )
        except KeyError:
            if campaign_name not in backtesting_by_optimizer_by_campaign:
                backtesting_by_optimizer_by_campaign[campaign_name] = {}
            if optimizer_id not in backtesting_by_optimizer_by_campaign[campaign_name]:
                backtesting_by_optimizer_by_campaign[campaign_name][optimizer_id] = {
                    backtesting_id
                }
    for (
        campaign_name,
        backtesting_by_optimizer,
    ) in backtesting_by_optimizer_by_campaign.items():
        for optimizer_id, backtests in backtesting_by_optimizer.items():
            run_db_identifier = databases.RunDatabasesIdentifier(
                trading_mode,
                optimization_campaign_name=campaign_name,
                backtesting_id=next(iter(backtests)),
                optimizer_id=optimizer_id,
            )
            async with databases.DBWriterReader.database(
                run_db_identifier.get_backtesting_metadata_identifier()
            ) as reader_writer:
                metadata = [
                    run
                    for run in await reader_writer.all(
                        commons_enums.DBTables.METADATA.value
                    )
                    if run[commons_enums.BacktestingMetadata.ID.value] not in backtests
                ]
                await reader_writer.replace_all(
                    commons_enums.DBTables.METADATA.value, metadata
                )