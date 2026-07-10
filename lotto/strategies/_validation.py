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
