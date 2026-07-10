import math


def parse_int_param(params: dict[str, str], name: str, default: str | None = None) -> int | None:
    raw_value = params.get(name, default)

    if raw_value is None:
        return None

    try:
        return int(raw_value)
    except ValueError as exc:
        raise ValueError(f'Parameter {name} must be an integer.') from exc


def parse_float_param(params: dict[str, str], name: str, default: str | None = None) -> float | None:
    raw_value = params.get(name, default)

    if raw_value is None:
        return None

    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f'Parameter {name} must be a number.') from exc

    if not math.isfinite(value):
        raise ValueError(f'Parameter {name} must be a number.')

    return value


def parse_float_between_param(
    params: dict[str, str],
    name: str,
    default: str,
    min_value: float,
    max_value: float,
) -> float:
    value = parse_float_param(params, name, default)

    if value is None:
        raise ValueError(f'Parameter {name} is required.')

    if value <= min_value or value >= max_value:
        raise ValueError(f'Parameter {name} must be greater than {min_value:g} and less than {max_value:g}.')

    return value


def parse_non_negative_int_param(params: dict[str, str], name: str, default: str) -> int:
    value = parse_int_param(params, name, default)

    if value is None:
        raise ValueError(f'Parameter {name} is required.')

    if value < 0:
        raise ValueError(f'Parameter {name} must be a non-negative integer.')

    return value


def parse_positive_int_param(params: dict[str, str], name: str, default: str) -> int:
    value = parse_int_param(params, name, default)

    if value is None:
        raise ValueError(f'Parameter {name} is required.')

    if value <= 0:
        raise ValueError(f'Parameter {name} must be a positive integer.')

    return value


def parse_numbers_param(params: dict[str, str], name: str, count: int, min_value: int, max_value: int) -> list[int]:
    raw_value = params.get(name)

    if raw_value is None:
        raise ValueError(f'Parameter {name} is required.')

    raw_numbers = [item.strip() for item in raw_value.split(',')]

    if len(raw_numbers) != count:
        raise ValueError(f'Parameter {name} must contain exactly {count} numbers.')

    try:
        numbers = [int(number) for number in raw_numbers]
    except ValueError as exc:
        raise ValueError(f'Parameter {name} must contain integers only.') from exc

    if any(number < min_value or number > max_value for number in numbers):
        raise ValueError(f'Parameter {name} must be in range {min_value}..{max_value}.')

    if len(set(numbers)) != count:
        raise ValueError(f'Parameter {name} must not contain duplicates.')

    return sorted(numbers)
