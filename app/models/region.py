from typing import Annotated,  Optional

from sqlmodel import Field,  SQLModel

class Region(SQLModel, table=True):
    region_id: Optional[int] = Field(default=None, primary_key=True)
    region_code:int
    region_name:str
    parent_region_id: Optional[int] = Field(default=None, foreign_key="region.region_id", nullable=True) 