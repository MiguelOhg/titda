from .base import Base, BaseMixin
from typing import List
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Perceptions(Base, BaseMixin):
    __tablename__ = 'its_perceptions'

    input = Column(String(50), unique=False, nullable=False)


class Plans(Base, BaseMixin):
    __tablename__ = 'its_plans'

    name = Column(String(50))
    description = Column(String(255))
    level = Column(String(50))
    actions: Mapped[List["Actions"]] = relationship()
    goal: Mapped["Goal"] = relationship(back_populates="its_plans")
    discrepancy: Mapped["Discrepancy"] = relationship(back_populates="its_plans")


class ProceduralMemory(Base, BaseMixin):
    __tablename__ = 'its_procedural_memory'

    name = Column(String(50))
    function_name = Column(String(255))
    params = Column(JSON())
    action_id: Mapped[int] = mapped_column(ForeignKey("its_actions.id"))
    action: Mapped["Actions"] = relationship(back_populates="its_actions")


class Actions(Base, BaseMixin):
    __tablename__ = 'its_actions'

    name = Column(String(50))
    description = Column(String(255))
    plan_id: Mapped[int] = mapped_column(ForeignKey("its_plans.id"))


class Goal(Base, BaseMixin):
    __tablename__ = 'its_goals'

    name = Column(String(50))
    description = Column(String(255))
    plan_id: Mapped[int] = mapped_column(ForeignKey("its_plans.id"))
    plan: Mapped["Plans"] = relationship(back_populates="its_plans")


class Discrepancy(Base, BaseMixin):
    __tablename__ = 'its_discrepancies'

    name = Column(String(50))
    description = Column(String(255))
    plan_id: Mapped[int] = mapped_column(ForeignKey("its_plans.id"))
    plan: Mapped["Plans"] = relationship(back_populates="its_plans")


class Response(Base, BaseMixin):
    __tablename__ = 'its_responses'


class Revision(Base, BaseMixin):
    __tablename__ = 'its_revisions'

