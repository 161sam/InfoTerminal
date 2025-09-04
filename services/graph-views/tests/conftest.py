import os

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("IT_JSON_LOGS", "1")
os.environ.setdefault("IT_ENV", "test")
os.environ.setdefault("IT_LOG_SAMPLING", "")
os.environ.setdefault("IT_OTEL", "1")
os.environ.setdefault("TESTING_OTEL_BOOT", "1")
