"""
Конфигурация
"""
import envparse

env = envparse.Env()

DB_ECHO = env.bool("DB_ECHO", default=False)
DB_FILE = env.str("DB_FILE", default="data.db")
