from typing import Optional

from sqlmodel import Field, SQLModel


class Link(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str
    short_url: str


class LinkUpdate(SQLModel):
    original_url: Optional[str] = None
    short_name: Optional[str] = None
