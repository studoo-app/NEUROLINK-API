from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Enum, ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from schemas.enums import Category, Severity, Tier

implant_incompatibilities = Table(
    "implant_incompatibilities",
    Base.metadata,
    Column(
        "implant_reference",
        ForeignKey("implants.reference"),
        primary_key=True,
    ),
    Column(
        "incompatible_implant_reference",
        ForeignKey("implants.reference"),
        primary_key=True,
    ),
)


class ImplantModel(Base):
    __tablename__ = "implants"

    reference: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[Category] = mapped_column(Enum(Category), nullable=False)
    tier: Mapped[Tier] = mapped_column(Enum(Tier), nullable=False)
    prerequisites: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    side_effects: Mapped[list[SideEffectModel]] = relationship(
        back_populates="implant",
        cascade="all, delete-orphan",
    )
    incompatible_implants: Mapped[list[ImplantModel]] = relationship(
        "ImplantModel",
        secondary=implant_incompatibilities,
        primaryjoin=reference == implant_incompatibilities.c.implant_reference,
        secondaryjoin=reference == implant_incompatibilities.c.incompatible_implant_reference,
    )


class SideEffectModel(Base):
    __tablename__ = "side_effects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    implant_reference: Mapped[str] = mapped_column(
        ForeignKey("implants.reference"),
        nullable=False,
        index=True,
    )
    reference: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    implant: Mapped[ImplantModel] = relationship(back_populates="side_effects")
