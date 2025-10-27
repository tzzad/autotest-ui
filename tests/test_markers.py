import pytest

@pytest.mark.smoke
def test_smoke_case():
    ...

@pytest.mark.regretion
def test_regretion_case():
    ...


class testsuit:
    @pytest.mark.smoke
    def test_regretion_case(self):
        ...

    @pytest.mark.smoke
    def test_smoke_case(self):
        ...