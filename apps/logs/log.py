import logging
import traceback


class DataBaseHandler(logging.Handler):
    def emit(self, record):
        from .models import Log

        trace = None
        if record.exc_info:
            trace = traceback.format_exc()

        kwargs = {"logger_name": record.name, "level": record.levelno, "msg": record.getMessage(), "trace": trace}
        Log.objects.create(**kwargs)
