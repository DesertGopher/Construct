from typing import List
from functools import wraps
from .api_logs import *
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def ex_handler(
    ex: Exception,
    object_name: str = "Объект",
    class_name: str = "Класс",
    method_name: str = "Метод",
    error_fields: List[str] = [],
) -> dict:
    ex_name = ex.__class__.__name__

    if ex_name == "EmptyResultSet":
        error_code = 2
    elif ex_name in ("ParseError", "DataError", "ValueError"):
        error_code = 3
    elif ex_name == "ValidationError":
        error_code = 4
    elif ex_name == "IntegrityError":
        error_code = 5
    elif ex_name in ("DoesNotExist", "ObjectDoesNotExist"):
        error_code = 6
    elif ex_name == "KeyError":
        error_code = 7
    elif ex_name == "TypeError":
        error_code = 8
    else:
        error_code = 1

    messages = {
        1: ex.args[0] if ex.args else "Неизвестная ошибка.",
        2: "Данные по запросу не найдены.",
        3: "Ошибка в формате данных. Проверьте правильность введенных данных.",
        4: f"Поля {error_fields} не указаны, либо указаны неверно. Проверьте правильность введенных данных.",
        5: f"{object_name} с таким id уже присутствует в базе данных.",
        6: f"{object_name} с таким id отсутствует в базе данных.",
        7: "Возможно отсутствует заголовок запроса или поле данных в теле запроса.",
        8: ex.args[0] if ex.args else "Неизвестная ошибка.",
    }

    error_root = f"Ошибка в {class_name}|{method_name}"

    return {"error_code": error_code, "message": f"{messages[error_code]} {error_root}"}


def exception_handler(object_name: str = "Объект"):
    """Декоратор для ловли и обработки ошибок в методах представлений."""

    def func_decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                log_request_created(api_view_logger, *args, **kwargs)
                result = method(self, *args, **kwargs)
                log_request_completed(api_view_logger, result, *args, **kwargs)
            except Exception as e:
                error_fields = []
                if isinstance(e, ValidationError):
                    error_fields = list(e.get_full_details().keys())
                error = ex_handler(
                    e,
                    object_name,
                    self.__class__.__name__,
                    method.__name__,
                    error_fields,
                )
                log_request_error(api_view_logger, e, error)
                return Response(error)
            else:
                return result

        return wrapper

    return func_decorator
