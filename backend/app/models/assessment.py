from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False,
    )

    semester_id: Mapped[int] = mapped_column(
        ForeignKey("semesters.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    maximum_marks: Mapped[float] = mapped_column(
        Numeric(5, 2),                              #Sandeep sir said for now consider maximum marks as 100, but in future we can change it to any value. So, I have used Numeric(5, 2) which means the maximum value can be 999.99 and minimum value can be 0.00.
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(
        Numeric(5, 2),
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