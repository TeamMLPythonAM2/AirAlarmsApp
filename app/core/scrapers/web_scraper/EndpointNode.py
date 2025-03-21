from pydantic import BaseModel
from consts import URL_PATTERN, ENDPOINT_PATTERN

class EndpointNode(BaseModel):
    base_url: URL_PATTERN
    endpoint_url: ENDPOINT_PATTERN
    content: bytes