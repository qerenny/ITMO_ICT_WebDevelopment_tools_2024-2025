import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel
from alembic import context

# Импортируем модели
from models.finance_models import User, Category, Transaction, Budget, Account, Goal, UserCategoryPreference

from dotenv import load_dotenv
load_dotenv()

# Получаем конфигурацию Alembic
config = context.config

# Берём URL БД из переменных окружения
config.set_main_option("sqlalchemy.url", os.environ["PR1_DB_URL"])

# Настраиваем логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata 

def run_migrations_offline() -> None:
    # Запуск миграций без подклчючения к БД.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Запуск миграций с подключением.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()