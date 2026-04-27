from sqlalchemy import create_engine, text


def create_database(db_name: str):
    engine = create_engine("postgresql://deep:1234@localhost:5432/postgres")

    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f'CREATE DATABASE "multitenant_{db_name}_db"'))
