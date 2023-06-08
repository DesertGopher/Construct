from loguru import logger
from django.conf import settings


# логгер для логирования всего лога Джанго
logger.add(
    settings.PATH_LOG / "logs.log",
    diagnose=False,
    backtrace=False,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} [{level}] {message}",
    level="DEBUG",
    rotation="1 MB",
    retention="7 days",
    compression="zip",
)
logger.bind(view=True)


# логгер для основных представлений
logger.add(
    settings.PATH_LOG / "server_logs.log",
    diagnose=False,
    backtrace=False,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} [{level}] {message}",
    level="DEBUG",
    rotation="1 MB",
    retention="7 days",
    compression="zip",
    filter=lambda record: "view" in record["extra"],
)
server_logger = logger.bind(view=True)


# логгер для АПИ методов
logger.add(
    settings.PATH_LOG / "api_view_logs.log",
    diagnose=False,
    backtrace=False,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} [{level}] {message}",
    level="DEBUG",
    rotation="1 MB",
    retention="7 days",
    compression="zip",
    filter=lambda record: "routers" in record["extra"],
)
api_view_logger = logger.bind(view=True)


# логгер для заказов
logger.add(
    settings.PATH_LOG / "orders_logs.log",
    diagnose=False,
    backtrace=False,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} [{level}] {message}",
    level="DEBUG",
    rotation="1 MB",
    retention="7 days",
    compression="zip",
    filter=lambda record: "orders" in record["extra"],
)
orders_logger = logger.bind(view=True)


def log_request_created(base_logger, request, *args, **kwargs):
    """Логирование информации о созданном запросе"""
    method_name = f"{request.method} {request.get_full_path()}"
    try:
        body = f"{request.data}"
    except Exception as e:
        body = f"{e}"
    # query = f'{dict(request.query_params)}'
    base_logger.info(f"Request: {method_name} Path kwargs:{kwargs} Body: {body}")


def log_request_completed(base_logger, response, request, *args, **kwargs):
    """Логирование информации об успешно выполненном запросе"""
    base_logger.success(f"Response: {response}")


def log_request_error(base_logger, exception, *args, **kwargs):
    """Логирование информации о неудачно выполненном запросе"""
    base_logger.error(f"Error: {exception}")
