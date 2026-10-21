def adapt_length(
    *,
    default_full_length: float,
    max_safe_length: float,
    length_taken_by_holder: float,
) -> float:
    """Limit tool length to the safe holder clearance."""
    if default_full_length + length_taken_by_holder > max_safe_length:
        return round(max_safe_length - length_taken_by_holder - 0.1, ndigits=3)
    else:
        return default_full_length


def adapt_flute_length(
    *, default_flute_length: float, full_length_adapted: float
) -> float:
    """Limit flute length to less than the adapted tool length."""
    if default_flute_length >= full_length_adapted:
        return round(full_length_adapted - 1, ndigits=3)
    else:
        return default_flute_length
