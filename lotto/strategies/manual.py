from ..core import AbstractStrategy, LottoDrawRecord, StrategyMetadata, StrategyRegistry
from ._params import parse_numbers_param

_metadata = StrategyMetadata(
    requires_data=False,
)


@StrategyRegistry.register('manual', _metadata)
class ManualStrategy(AbstractStrategy):
    def __init__(self, params: dict[str, str]) -> None:
        self._numbers = parse_numbers_param(params, 'numbers', self.TAKE, 1, self.POOL_MAX)

    def prepare_data(self, _: list[LottoDrawRecord]) -> None:
        pass

    def generate_numbers(self) -> list[int]:
        return list(self._numbers)
