from pydantic import BaseModel, Field


class PongResponse(BaseModel):
    message: str = Field(default='Pong!')
