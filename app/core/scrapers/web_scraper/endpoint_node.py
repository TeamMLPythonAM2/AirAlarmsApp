from consts import ENDPOINT_PATTERN, URL_PATTERN
from pydantic import BaseModel


class EndpointNode(BaseModel):
    base_url: URL_PATTERN
    endpoint_url: ENDPOINT_PATTERN
    content: bytes
