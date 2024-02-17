"""
Token schema for validate jwt token
"""

from pydantic import BaseModel


class TokenInfo(BaseModel):
    """
    Schema for get bearer token information
    for default it's Bearer token type
    """

    access_token: str
    type_token: str
