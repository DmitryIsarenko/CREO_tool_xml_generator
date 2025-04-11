def adapt_length(*, default_full_length: float, max_safe_length: float, length_taken_by_holder: float) -> float:
    """
    Эта ф-я используется при генерации XML файла инструмента для токарно-фразерного инструмента.
    Эта ф-я принимает на вход стоковую длину инструмента, максимально безопасную для данной оправки длину инструмента и
    длину, которую съедает оправка от этой максимльано возможной безопасной длины.
    Эта ф-я возвращает длину инструмента, максимально допустимую для данной оправки, если стоковая её превышала.
    Если стоковая не превышала - то ничего не изменяет.

    :param default_full_length:
    :param max_safe_length:
    :param length_taken_by_holder:
    :return:
    """
    if default_full_length + length_taken_by_holder > max_safe_length:
        return round(max_safe_length - length_taken_by_holder - 0.1, ndigits=3)
    else:
        return default_full_length

def adapt_flute_length(*, default_flute_length: float, full_length_adapted: float) -> float:
    """
    Эта ф-я снижает длину режущей кромки инструмента для вставки в XML инструмента, если её длина оказалась больше
    общей длины инструмента
    :param default_flute_length:
    :param full_length_adapted:
    :return:
    """

    if default_flute_length >= full_length_adapted:
        return round(full_length_adapted - 1, ndigits=3)
    else:
        return default_flute_length