from pydantic import BaseModel, Field


class LoginForm(BaseModel):
    username: str = Field()
    serverkey: str = Field()
