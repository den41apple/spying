"""
Валидаторы
"""
import validators
from validators import ValidationError


def is_valid_url(url: str) -> bool:
    """
    Проверяет валидность ссылки

    Возвращает:
    -----------
        bool
    """
    result = validators.url(url)
    if isinstance(result, ValidationError):
        return False
    return True


def validate_visited_domains_params(_from: int | None = None,
                                    to: int | None = None) -> str:
    """
    Проверяет параметры запроса для эндпоинта "/visited_domains"

    Параметры:
    ----------
        _from: int | None - Число в timestamp
                            для фильтрации левой границы времени (Включительно)
        to: int | None - Число в timestamp
                         для фильтрации правой границы времени (Включительно)


    Возвращает:
    -----------
        str - Строка будет содержать текст если имеется ошибка
    """
    errors = []
    error_string = ""
    if _from is not None:
        if _from < 0:
            errors.append('"from" должен быть больше нуля')
    if to is not None:
        if to < 0:
            errors.append('"to" должен быть больше нуля')
    if _from is not None and to is not None:
        if _from > to:
            errors.append('"from" должен быть меньше "to"')
    if errors:
        error_string += "Ошибк"
        if len(errors) > 1:
            error_string += "и: "
        else:
            error_string += "а: "
        for i, el in enumerate(errors):
            if len(errors) > 1:
                error_string += f"{i + 1})"
            error_string += el
            if len(errors) > 1:
                error_string += ". "
    return error_string.strip()
