from limit_order_sdk.validations import is_int


class Pager:
    def __init__(self, limit=100, page=1):
        assert is_int(limit) and limit > 0, "Invalid limit"
        assert is_int(page) and page > 0, "Invalid page"

        self.limit = limit
        self.page = page
