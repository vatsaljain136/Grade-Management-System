from datetime import datetime

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Course(Base):
    __tablename__ = "courses"
                                            #Mapped[int] means the expected type of the attribute is an integer
    id: Mapped[int] = mapped_column(        #mapped_column() is(basically constraints) a function provided by SQLAlchemy that allows you to define the properties of a column in the database table. 
        primary_key=True,
        autoincrement=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    credits: Mapped[float] = mapped_column(
        Numeric(4, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )