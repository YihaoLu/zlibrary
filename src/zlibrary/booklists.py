from .abs import BooklistPaginator
from enum import Enum
from typing import List


class OrderOptions(Enum):
    POPULAR = "popular"
    NEWEST = "date_created"
    RECENT = "date_updated"


class Booklists:
    __r = None
    cookies = {}
    mirror = None

    def __init__(self, request, cookies, mirror):
        self.__r = request
        self.cookies = cookies
        self.mirror = mirror

    async def search_public(self, q: str = "", count: int = 10, order: OrderOptions = "", lang: List[str] = []):
        url = self.mirror + '/booklists?searchQuery=%s&order=%s' % (q, order.value)
        if lang:
            assert type(lang) is list
            for l in lang:
                url += '&languages%5B%5D={}'.format(l)
        paginator = BooklistPaginator(url, count, self.__r, self.mirror)
        return await paginator.init()

    async def search_private(self, q: str = "", count: int = 10, order: OrderOptions = "", lang: List[str] = []):
        url = self.mirror + '/booklists/my?searchQuery=%s&order=%s' % (q, order.value)
        if lang:
            assert type(lang) is list
            for l in lang:
                url += '&languages%5B%5D={}'.format(l)
        paginator = BooklistPaginator(url, count, self.__r, self.mirror)
        return await paginator.init()
