from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from src.sql.dbSettings import Base, Engine

# Alembic Configオブジェクト
config = context.config

# ロギングの設定
fileConfig(config.config_file_name)

# モデルのMetaDataオブジェクトを追加
target_metadata = Base.metadata


def run_migrations_offline():
    """オフラインモードでマイグレーションを実行します。"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """オンラインモードでマイグレーションを実行します。"""
    url = config.get_main_option("sqlalchemy.url")
    connectable = Engine

    with connectable.connect() as connection:
        context.configure(
            url=url, connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# モードに応じてマイグレーションを実行
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
