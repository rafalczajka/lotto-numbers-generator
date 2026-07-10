def parse_int_param(params: dict[str, str], name: str, default: str | None = None) -> int | None:
    raw_value = params.get(name, default)

    if raw_value is None:
        return None

    try:
        return int(raw_value)
    except ValueError as exc:
        raise ValueError(f'Parameter {name} must be an integer.') from exc


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
