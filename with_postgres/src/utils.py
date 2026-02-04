import datetime


def write_log(message: str):
    """
    Background task to write log message
    """
    with open("app.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now(datetime.timezone.utc)}: {message}\n")
