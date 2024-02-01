"""
Конфигурация
"""
import envparse

env = envparse.Env()

DB_ECHO = env.bool("DB_ECHO", default=False)
DB_URL = env.str("DB_URL", default="sqlite+aiosqlite:///data.db")
