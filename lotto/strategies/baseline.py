import random

from ..core import AbstractStrategy, LottoDrawRecord, StrategyMetadata, StrategyRegistry
from ._params import parse_int_param

_metadata = StrategyMetadata(
    requires_data=False,
)


@StrategyRegistry.register('random', _metadata)
class Baseline(AbstractStrategy):
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
