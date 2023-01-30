from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
import os


engine = create_engine(
    settings.database_url,
    # connect_args={'check_same_thread': False},
)


Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
