from bs4 import BeautifulSoup
import requests
from fastapi import HTTPException
from pydantic import BaseModel, validate_call
from consts import URL_PATTERN, ENDPOINT_PATTERN
from EndpointNode import EndpointNode


class WebScraper(BaseModel):
    base_url: URL_PATTERN = None
    # endpoint_node: type[EndpointNode] = None

    @validate_call
    def get_page_content(self, endpoint: ENDPOINT_PATTERN) -> EndpointNode:
        response = requests.get(self.base_url + endpoint)
        if response.status_code == 200:
            return EndpointNode(
                base_url=self.base_url,
                endpoint_url=endpoint,
                content=response.content
            )
        # TODO need sth better that HTTPException
        raise HTTPException(
            status_code=404,
            detail=f"WebScraper.py / get_page() / request {self.base_url + endpoint} fail"
        )

    def cook_soup(self, node: EndpointNode):
        soup = BeautifulSoup(node.content, 'html.parser')




if __name__ == "__main__":
    dd = {"base_url": "http"}
    scr = WebScraper(**dd)
    print(scr)
