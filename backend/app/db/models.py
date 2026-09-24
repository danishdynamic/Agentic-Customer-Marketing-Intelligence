from datetime import date, datetime
from decimal import Decimal

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    campaign_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    campaign_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    ads: Mapped[list["Ad"]] = relationship(
        back_populates="campaign",
        cascade="all, delete-orphan",
    )


class Ad(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    ad_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id"),
        nullable=False,
        index=True,
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # Performance metrics

    impressions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reach: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    clicks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    spend: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    conversions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    conversion_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    ctr: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
    )

    cpc: Mapped[Decimal] = mapped_column(
        Numeric(10, 4),
        nullable=False,
    )

    cpa: Mapped[Decimal] = mapped_column(
        Numeric(10, 4),
        nullable=False,
    )

    roas: Mapped[Decimal] = mapped_column(
        Numeric(10, 4),
        nullable=False,
    )

    # Targeting

    audience: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    age_group: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    gender: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    device: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    placement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Marketing content

    headline: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    primary_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    call_to_action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    marketing_angle: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    tone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    offer_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    product_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    campaign: Mapped["Campaign"] = relationship(
        back_populates="ads",
    )

    document: Mapped["AdDocument | None"] = relationship(
        back_populates="ad",
        uselist=False,
        cascade="all, delete-orphan",
    )


class AdDocument(Base):
    __tablename__ = "ad_documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    ad_id: Mapped[int] = mapped_column(
        ForeignKey("ads.id"),
        unique=True,
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(768),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    ad: Mapped["Ad"] = relationship(
        back_populates="document",
    )