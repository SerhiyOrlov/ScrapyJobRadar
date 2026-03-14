from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    location: Mapped[str]
    site: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="company")


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String))
    posted_at: Mapped[datetime]
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="vacancies")
    description: Mapped[str]
    external_id: Mapped[str]
    source: Mapped[str]
    url: Mapped[str]
    salary_from: Mapped[int] = mapped_column(nullable=True)
    salary_to: Mapped[int] = mapped_column(nullable=True)
    skills: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
