from collections import Counter

from ..core import AbstractStrategy, StrategyMetadata, StrategyRegistry
from ._params import parse_non_negative_int_param

_default_params = {
    'lookback': '100',
}


_metadata = StrategyMetadata()


@StrategyRegistry.register('hot-numbers', _metadata)
class HotNumbers(AbstractStrategy):
    """
    Pick the six numbers from 1 to 49 that appeared most often in past draws.

    Available as 'hot-numbers', this strategy counts how often each number
    appears in the selected draws and picks those with the highest
    counts. Every appearance counts equally, regardless of how recent it is.
    The supplied history can contain Lotto or Lotto Plus draws.

    Parameters:
        lookback: Number of recent draws to consider. Defaults to 100.
            Use 0 to include all available draws. If fewer draws are
            available than requested, all of them are used.

    When numbers have the same count, the one encountered first while
    reading the selected draws is picked first. This also depends on the
    order of numbers within each draw. If fewer than six different numbers
    appeared, the remaining places are filled with unused numbers from
    smallest to largest.

    With no history, the strategy returns 1 through 6. The same history in
    the same order and the same parameters always produce the same result.
    Results are returned from smallest to largest.
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

        ranked = [n for n, _ in counter.most_common()]
        pool = list(range(1, self.POOL_MAX + 1))
        ranked += [n for n in pool if n not in ranked]

        pick = ranked[: self.TAKE]
        pick.sort()

        return pick
