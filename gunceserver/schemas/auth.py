from pydantic import BaseModel
from typing import Optional
from fastapi.param_functions import Form


class LoginForm(BaseModel):
    username: str = Form()
    serverkey: str = Form()
