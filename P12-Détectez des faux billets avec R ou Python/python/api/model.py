from pydantic import BaseModel, Field

class BillRequest(BaseModel):
    diagonal: float = Field(..., ge=170, le=175, description="Between 170 and 174")
    height_left: float = Field(..., ge=102, le=106, description="Between 102 and 106")
    height_right: float = Field(..., ge=101, le=106, description="Between 101 and 106")
    margin_low: float = Field(..., ge=2.5, le=7.5, description="Between 2.5 and 7.5")
    margin_up: float = Field(..., ge=2, le=4, description="Between 2 and 4")
    length: float = Field(..., ge=108, le=115, description="Between 108 and 115")
