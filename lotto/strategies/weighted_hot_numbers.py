from collections import Counter

from ..core import AbstractStrategy, StrategyMetadata, StrategyRegistry
from ._params import parse_non_negative_int_param

_default_params = {
    'lookback': '100',
}


_metadata = StrategyMetadata()


@StrategyRegistry.register('weighted-hot-numbers', _metadata)
class WeightedHotNumbers(AbstractStrategy):
    """
    Pick six numbers from 1 to 49, giving more points to recent appearances.

    Available as 'weighted-hot-numbers', this strategy adds points each time
    a number appears in the selected draws. The oldest selected draw
    adds 1 point, the next adds 2, and so on. With 100 draws, the latest draw
    adds 100 points. The six numbers with the most points are picked.
    Weights increase by 1 per draw, regardless of the time between draws.
    The supplied history can contain Lotto or Lotto Plus draws.

    Parameters:
        lookback: Number of recent draws to consider. Defaults to 100.
            Use 0 to include all available draws. If fewer draws are
            available than requested, all of them are used. The latest
            draw's weight equals the number of draws actually used.

    When numbers have the same score, the smaller number is picked first.
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

        for weight, numbers in enumerate(draws, start=1):
            for number in numbers:
                if 1 <= number <= self.POOL_MAX:
                    counter[number] += weight

        ranked = sorted(range(1, self.POOL_MAX + 1), key=lambda number: (-counter.get(number, 0), number))
        pick = ranked[: self.TAKE]
        pick.sort()

        return pick
