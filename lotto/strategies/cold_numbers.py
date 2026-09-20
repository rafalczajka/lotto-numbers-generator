from collections import Counter

from ..core import AbstractStrategy, StrategyMetadata, StrategyRegistry
from ._params import parse_non_negative_int_param

_default_params = {
    'lookback': '100',
}


_metadata = StrategyMetadata()


@StrategyRegistry.register('cold-numbers', _metadata)
class ColdNumbers(AbstractStrategy):
    """
    Pick the six numbers from 1 to 49 that appeared least often in past draws.

    Available as 'cold-numbers', this strategy counts how often each number
    appears in the selected draws and picks those with the lowest counts.
    Numbers that did not appear at all are picked first. The supplied history
    can contain Lotto or Lotto Plus draws.

    Parameters:
        lookback: Number of recent draws to consider. Defaults to 100.
            Use 0 to include all available draws. If fewer draws are
            available than requested, all of them are used.

    When numbers have the same count, the smaller number is picked first.
    With no history, the strategy returns 1 through 6. The same history and
    parameters always produce the same result, sorted from smallest to largest.
    """

    def __init__(self, params: dict[str, str]) -> None:
        self._lookback = parse_non_negative_int_param(params, 'lookback', _default_params['lookback'])
        self._draws: list[list[int]] = []

    def prepare_data(self, draws: list[list[int]]) -> None:
        self._draws = draws

    def generate_numbers(self) -> list[int]:
        draws = self._draws[-self._lookback :] if self._lookback else self._draws
        counter = Counter()

        for numbers in draws:
            counter.update([n for n in numbers if 1 <= n <= self.POOL_MAX])

        ranked = sorted(range(1, self.POOL_MAX + 1), key=lambda number: (counter.get(number, 0), number))
        pick = ranked[: self.TAKE]
        pick.sort()

        return pick
