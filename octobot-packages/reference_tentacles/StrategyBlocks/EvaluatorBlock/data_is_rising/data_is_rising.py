import octobot_commons.enums as commons_enums
import tentacles.Meta.Keywords.indicator_keywords.moving.moving_up_down as moving_up_down
import tentacles.Meta.Keywords.block_factory.block_factory_enums as block_factory_enums
import tentacles.Meta.Keywords.block_factory.abstract_evaluator_block as abstract_evaluator_block


class DataIsRisingEvaluator(abstract_evaluator_block.EvaluatorBlock):
    NAME = "data_is_rising"
    TITLE = "Data is rising"
    TITLE_SHORT = TITLE
    DESCRIPTION = (
        "Data is rising, takes a single data source "
        "and gives you signals when it is rising."
    )
    signal_lag: int
    sideways_is_rising: bool
    only_one_signal: bool

    def init_block_settings(self) -> None:
        selected_indicator = self.activate_single_input_data_node(
            enable_static_value=False
        )
        self.signal_lag = self.user_input(
            name="Amount of consecutive rising candles before flashing a signal",
            input_type=commons_enums.UserInputTypes.INT,
            def_val=2,
            min_val=1,
            grid_columns=12,
        )
        self.sideways_is_rising = self.user_input(
            name="Sideways counts as rising",
            input_type=commons_enums.UserInputTypes.BOOLEAN,
            def_val=True,
            grid_columns=12,
        )
        self.only_one_signal = self.user_input(
            name="Flash signals only on the first candle",
            input_type=commons_enums.UserInputTypes.BOOLEAN,
            def_val=False,
            grid_columns=12,
        )
        self.register_evaluator_data_output(
            title="Rising Signals",
            plot_switch_text=f"Plot when data source is rising",
            plot_color_switch_title="Signals plot color",
            default_plot_color=block_factory_enums.Colors.GREEN,
            allow_move_signal_to_the_right=True,
        )

    async def execute_block(
        self,
    ) -> None:
        (
            data_source_values,
            chart_location,
            indicator_title,
        ) = await self.get_input_node_data()
        signals = moving_up_down.moving_up(
            data_source_values,
            self.signal_lag,
            sideways_is_rising=self.sideways_is_rising,
            only_first_signal=self.only_one_signal,
        )
        await self.store_evaluator_signals(
            title=f"{indicator_title} is rising",
            signals=signals,
            signal_values=data_source_values,
            chart_location=chart_location,
        )
