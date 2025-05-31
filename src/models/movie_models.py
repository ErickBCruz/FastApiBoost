from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime

# modelos movie

class Movie(BaseModel):
    id: Optional[int]
    title: str
    category: str
    year: int


class MovieUpdate(BaseModel):
    title: str
    category: str
    year: int

class MovieCreate(BaseModel):
    id: int
    title: str # = Field(min_length=5, max_length=15, default="My movie") #validaciones de datos
    category: str = Field(default="My category")
    year: int = Field(le=datetime.date.today().year, ge= 1900, default=2000)

    model_config = {
        "json_schema_extra":{
            "example":{
                "id": 1,
                "title": "my movie",
                "category": "my category",
                "year": 2025,
            }
        }
    }

    @field_validator("title")      #Errores personalizados
    @classmethod
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError("La longitud es menor de 5")
        elif len(value) > 15:
            raise ValueError("la longitud es mayor a 15")
        return value