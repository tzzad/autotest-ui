import pytest

@pytest.mark.smoke
def test_smoke_case():
    ...

@pytest.mark.regretion
def test_regretion_case():
    ...


class testsuit:
    @pytest.mark.smokek
    def test_regretion_case(self):
        ...

    @pytest.mark.smokig
    def test_smoke_case(self):
        ...