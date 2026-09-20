from collections import Counter

from ..core import AbstractStrategy, LottoDrawRecord, StrategyMetadata, StrategyRegistry
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
    appears in the selected Lotto draws and picks those with the lowest
    counts. Numbers that did not appear at all are picked first. Lotto Plus
    results are not used.

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
        self._data: list[LottoDrawRecord] = []

    def prepare_data(self, data: list[LottoDrawRecord]) -> None:
        self._data = data

    def generate_numbers(self) -> list[int]:
        draws = self._data[-self._lookback :] if self._lookback else self._data
        counter = Counter()

        for record in draws:
            counter.update([n for n in record.lotto_numbers if 1 <= n <= self.POOL_MAX])

        ranked = sorted(range(1, self.POOL_MAX + 1), key=lambda number: (counter.get(number, 0), number))
        pick = ranked[: self.TAKE]
        pick.sort()

        return pick
