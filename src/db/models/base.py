"""
Main database instance which has metadata
All models must be inherited from this
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
