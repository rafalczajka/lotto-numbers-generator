import random

from ..core import AbstractStrategy, LottoDrawRecord, StrategyMetadata, StrategyRegistry

_metadata = StrategyMetadata(
    requires_data=False,
)


@StrategyRegistry.register('random', _metadata)
class Baseline(AbstractStrategy):
    def __init__(self, params: dict[str, str]) -> None:
        seed_param = params.get('seed')

        if seed_param is None:
            self._rng = random.Random()
            return

        try:
            seed = int(seed_param)
        except ValueError as exc:
            raise ValueError('Parameter seed must be an integer.') from exc

        self._rng = random.Random(seed)

    def prepare_data(self, _: list[LottoDrawRecord]) -> None:
        pass

    def generate_numbers(self) -> list[int]:
        numbers = self._rng.sample(range(1, self.POOL_MAX + 1), k=self.TAKE)
        numbers.sort()
        return numbers
