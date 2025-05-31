from pydantic import BaseModel
from typing import Optional

class GameCreate(BaseModel):
    id: int
    title: str
    category: str
    year: int

    model_config = {
        "json_schema_extra":{
            "example":{
                "id": 1,
                "title": "my game",
                "category": "my category",
                "year": 2025,
            }
        }
    }
    # validaciones mediante model_config

#gt greater than
#ge greater than or equal
#lt less than
#le less than or equal

class Game(BaseModel):
    id: Optional[int]
    title: str
    category: str
    year: int