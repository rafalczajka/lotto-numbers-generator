from ..core import AbstractRankedStrategy, AbstractStrategy, StrategyMetadata, StrategyRegistry
from .decay_hot_numbers import DecayHotNumbers
from .overdue_numbers import OverdueNumbers
from .rising_numbers import RisingNumbers

_metadata = StrategyMetadata()


def _remap_params(params: dict[str, str], mapping: dict[str, str]) -> dict[str, str]:
    return {target: params[source] for source, target in mapping.items() if source in params}


@StrategyRegistry.register('balanced-mix', _metadata)
class BalancedMix(AbstractStrategy):
    """
    Pick six different numbers from 1 to 49 by combining three strategies.

    Available as 'balanced-mix', this strategy takes two numbers from each of
    decay-hot-numbers, rising-numbers, and overdue-numbers. They favor recent
    appearances, a recent rise in frequency, and a long gap since the last
    appearance, respectively. All three use the same source of history,
    which can contain Lotto or Lotto Plus draws.

    Numbers are picked one at a time in this order: decay, rising, overdue,
    overdue, rising, decay. Each strategy supplies its highest-ranked number
    that has not already been picked. If a number is already in the set,
    selection moves to the next number in that strategy's ranking. Each
    strategy keeps its own rules for resolving ties.

    Parameters:
        decay_lookback: Number of recent draws used by decay-hot-numbers.
            Defaults to 100. Use 0 to include all available draws.
        decay: Weight multiplier for each older draw in decay-hot-numbers.
            Must be greater than 0 and less than 1. Defaults to 0.95.
            Lower values give recent draws more importance.
        rising_short_lookback: Number of recent draws used to measure the
            recent frequency in rising-numbers. Must be positive.
            Defaults to 20.
        rising_long_lookback: Number of recent draws used for comparison
            in rising-numbers. Must be greater than rising_short_lookback.
            Defaults to 100.
        overdue_lookback: Number of recent draws used by overdue-numbers.
            Defaults to 100. Use 0 to include all available draws.

    All three strategies receive the same history and use their own windows.
    If fewer draws are available than requested, they use what is available.
    With no history, the mix returns 1 through 6. The same history and
    parameters always produce the same result, sorted from smallest to largest.
    """

    def __init__(self, params: dict[str, str]) -> None:
        decay = DecayHotNumbers(
            _remap_params(
                params,
                {
                    'decay_lookback': 'lookback',
                    'decay': 'decay',
                },
            )
        )
        rising = RisingNumbers(
            _remap_params(
                params,
                {
                    'rising_short_lookback': 'short_lookback',
                    'rising_long_lookback': 'long_lookback',
                },
            )
        )
        overdue = OverdueNumbers(
            _remap_params(
                params,
                {
                    'overdue_lookback': 'lookback',
                },
            )
        )

        self._strategies: tuple[AbstractRankedStrategy, ...] = (decay, rising, overdue)
        self._selection_order = (decay, rising, overdue, overdue, rising, decay)

    def prepare_data(self, draws: list[list[int]]) -> None:
        for strategy in self._strategies:
            strategy.prepare_data(draws)

    def generate_numbers(self) -> list[int]:
        rankings = {strategy: strategy.rank_numbers() for strategy in self._strategies}
        selected: set[int] = set()

        for strategy in self._selection_order:
            number = next(number for number in rankings[strategy] if number not in selected)
            selected.add(number)

        return sorted(selected)
