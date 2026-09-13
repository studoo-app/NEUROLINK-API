from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Enum, ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from schemas.enums import Category, Severity, Tier, ApiKeyRole

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
    description: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
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

class ApiKeyModel(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    key_id: Mapped[str] = mapped_column(String(20),unique=True,index=True,)
    key_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[ApiKeyRole] = mapped_column(Enum(ApiKeyRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)