from collections import Counter

from ..core import AbstractRankedStrategy, LottoDrawRecord, StrategyMetadata, StrategyRegistry
from ._params import parse_float_between_param, parse_non_negative_int_param

_default_params = {
    'lookback': '100',
    'decay': '0.95',
}


_metadata = StrategyMetadata()


@StrategyRegistry.register('decay-hot-numbers', _metadata)
class DecayHotNumbers(AbstractRankedStrategy):
    """
    Pick six numbers from 1 to 49, giving more importance to recent draws.

    Available as 'decay-hot-numbers', this strategy adds points each time a
    number appears in the selected Lotto draws. The latest draw adds 1 point,
    the previous draw adds decay points, the one before adds decay ** 2,
    and so on. The six numbers with the most points are picked. Age is counted
    in draws, not days. Lotto Plus results are not used.

    Parameters:
        lookback: Number of recent draws to consider. Defaults to 100.
            Use 0 to include all available draws. If fewer draws are
            available than requested, all of them are used.
        decay: How much of a draw's weight is kept for each step back in
            history. Must be greater than 0 and less than 1. Defaults to 0.95.
            Lower values give recent draws more importance. Values closer
            to 1 let older draws contribute more.

    When numbers have the same score, the smaller number is picked first.
    With no history, the strategy returns 1 through 6. The same history and
    parameters always produce the same result, sorted from smallest to largest.
    """

    def __init__(self, params: dict[str, str]) -> None:
        self._lookback = parse_non_negative_int_param(params, 'lookback', _default_params['lookback'])
        self._decay = parse_float_between_param(params, 'decay', _default_params['decay'], 0, 1)
        self._data: list[LottoDrawRecord] = []

    def prepare_data(self, data: list[LottoDrawRecord]) -> None:
        self._data = data

    def rank_numbers(self) -> list[int]:
        draws = self._data[-self._lookback :] if self._lookback else self._data
        counter = Counter()

        for age, record in enumerate(reversed(draws)):
            weight = self._decay**age

            for number in record.lotto_numbers:
                if 1 <= number <= self.POOL_MAX:
                    counter[number] += weight

        return sorted(range(1, self.POOL_MAX + 1), key=lambda number: (-counter.get(number, 0), number))
