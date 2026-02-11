from pydantic import BaseModel, Field
from typing import List, Union, Optional

class ExtractedItem(BaseModel):
    product_name: Optional[str] = Field(None, description="Name of the product")
    quantity: Optional[float] = Field(None, description="Quantity of the product")
    unit: Optional[str] = Field(None, description="Unit of measurement for the quantity (e.g., kg, pcs, bottles)")
    price: Optional[float] = Field(None, description="Total price for the product line")
    unit_price: Optional[float] = Field(None, description="Price per unit of the product")

class ParseRequest(BaseModel):
    content: Union[str, List[str]] = Field(..., description="Invoice content as a single string or a list of strings")

class ParseResponse(BaseModel):
    extracted_items: List[ExtractedItem] = Field(..., description="List of extracted items from the invoice content")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")