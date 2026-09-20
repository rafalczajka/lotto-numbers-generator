import datetime
from collections.abc import Iterator

from .core import AbstractStrategy, GameRecord, GameType, LottoDrawRecord, select_draw_numbers


class BacktestEngine:
    def __init__(self, strategy: AbstractStrategy, lotto_plus: bool = False) -> None:
        self._history: list[GameRecord] = []
        self._strategy = strategy
        self._lotto_plus = lotto_plus

    @property
    def history(self) -> list[GameRecord]:
        return self._history

    def run(self, data: list[LottoDrawRecord]) -> list[GameRecord]:
        return list(self.results_gen(data))

    def results_gen(self, data: list[LottoDrawRecord]) -> Iterator[GameRecord]:
        self._history = []
        sorted_data = sorted(data, key=lambda record: record.draw_date)

        for index, record in enumerate(sorted_data):
            draws = select_draw_numbers(sorted_data[:index], self._lotto_plus)
            self._strategy.prepare_data(draws)

            for game_type, draw_result in self._get_game_results(record):
                yield self._handle_game(record.draw_date, game_type, draw_result)

    def _handle_game(self, draw_date: datetime.date, game_type: GameType, draw_result: list[int]) -> GameRecord:
        generated_numbers = self._strategy.generate_numbers()
        matches = self._count_matches(draw_result, generated_numbers)

        new_record = GameRecord(
            game_type=game_type,
            draw_date=draw_date,
            draw_result=draw_result,
            generated_numbers=generated_numbers,
            matches=matches,
        )

        self._history.append(new_record)
        return new_record

    def _count_matches(self, draw_result: list[int], generated_numbers: list[int]) -> int:
        return len(set(draw_result) & set(generated_numbers))

    def _get_game_results(self, record: LottoDrawRecord) -> Iterator[tuple[GameType, list[int]]]:
        yield GameType.LOTTO, record.lotto_numbers

        if record.plus_numbers:
            yield GameType.LOTTO_PLUS, record.plus_numbers
