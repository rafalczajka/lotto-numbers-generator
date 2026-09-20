from ..core import AbstractRankedStrategy, StrategyMetadata, StrategyRegistry
from ._params import parse_non_negative_int_param

_default_params = {
    'lookback': '100',
}


_metadata = StrategyMetadata()


@StrategyRegistry.register('overdue-numbers', _metadata)
class OverdueNumbers(AbstractRankedStrategy):
    """
    Pick six numbers from 1 to 49 that have not appeared for the longest time.

    Available as 'overdue-numbers', this strategy checks when each number last
    appeared in the selected draws. Numbers that did not appear in those
    draws are picked first, followed by those whose last appearance was
    furthest back. Only the last appearance matters, not how often a number
    appeared. Time is measured in draws, not days. The supplied history can
    contain Lotto or Lotto Plus draws.

    Parameters:
        lookback: Number of recent draws to consider. Defaults to 100.
            Use 0 to include all available draws. If fewer draws are
            available than requested, all of them are used.

    Numbers last seen in the same draw are ordered from smallest to largest.
    The same rule applies to numbers missing from the selected history;
    appearances before that window are not considered.

    With no history, the strategy returns 1 through 6. The same history and
    parameters always produce the same result, sorted from smallest to largest.
    """

    def __init__(self, params: dict[str, str]) -> None:
        self._lookback = parse_non_negative_int_param(params, 'lookback', _default_params['lookback'])
        self._draws: list[list[int]] = []

    def prepare_data(self, draws: list[list[int]]) -> None:
        self._draws = draws

    def rank_numbers(self) -> list[int]:
        draws = self._draws[-self._lookback :] if self._lookback else self._draws
        last_seen_index: dict[int, int] = {}

        for index, numbers in enumerate(draws):
            for number in numbers:
                if 1 <= number <= self.POOL_MAX:
                    last_seen_index[number] = index

        return sorted(
            range(1, self.POOL_MAX + 1),
            key=lambda number: (number in last_seen_index, last_seen_index.get(number, -1), number),
        )
