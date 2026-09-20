from ..core import AbstractStrategy, StrategyMetadata, StrategyRegistry
from ._params import parse_numbers_param

_metadata = StrategyMetadata(
    requires_data=False,
)


@StrategyRegistry.register('manual', _metadata)
class ManualStrategy(AbstractStrategy):
    """
    Use six numbers of your choice from 1 to 49.

    Available as 'manual', this strategy lets you use a fixed set of numbers,
    for example to check how it would have performed in past draws. It does
    not use draw history to choose or change the numbers.

    Parameters:
        numbers: Required list of six different integers separated by commas,
            for example '3,12,19,27,35,48'. Each number must be from 1 to 49.
            Spaces around numbers are allowed. There is no default set.

    Missing or invalid numbers cause an error when the strategy is created.
    Every call returns the same six numbers, sorted from smallest to largest,
    including when no history exists.
    """

    def __init__(self, params: dict[str, str]) -> None:
        self._numbers = parse_numbers_param(params, 'numbers', self.TAKE, 1, self.POOL_MAX)

    def prepare_data(self, _: list[list[int]]) -> None:
        pass

    def generate_numbers(self) -> list[int]:
        return list(self._numbers)
