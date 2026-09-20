import random

from ..core import AbstractStrategy, LottoDrawRecord, StrategyMetadata, StrategyRegistry
from ._params import parse_int_param

_metadata = StrategyMetadata(
    requires_data=False,
)


@StrategyRegistry.register('random', _metadata)
class Baseline(AbstractStrategy):
    """
    Pick six different random numbers from 1 to 49.

    Available as 'random', this strategy is a simple starting point for
    comparing other strategies. Every set of six numbers has the same chance
    of being picked. Past draw results do not affect the selection, so the
    strategy works without any history.

    Parameters:
        seed: Optional integer that makes results repeatable. Two new
            instances using the same seed produce the same sequence of sets.
            When omitted, the random generator chooses its own starting state.

    Each call picks another set, even when a seed is provided. A number cannot
    appear twice in one set, but it can appear again in later sets. Results
    are returned from smallest to largest.
    """

    def __init__(self, params: dict[str, str]) -> None:
        seed = parse_int_param(params, 'seed')

        if seed is None:
            self._rng = random.Random()
            return

        self._rng = random.Random(seed)

    def prepare_data(self, _: list[LottoDrawRecord]) -> None:
        pass

    def generate_numbers(self) -> list[int]:
        numbers = self._rng.sample(range(1, self.POOL_MAX + 1), k=self.TAKE)
        numbers.sort()
        return numbers
