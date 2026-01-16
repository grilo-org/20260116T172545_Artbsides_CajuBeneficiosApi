from api.modules.merchants.v1.enums.category_codes import CategoryCodes


class TestCategoryCodes:
    def category_codes_successful_test(self) -> None:
        assert CategoryCodes.list() is not None
