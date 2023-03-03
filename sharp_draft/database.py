from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings


engine = create_engine(
    settings.database_url,
)


Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
