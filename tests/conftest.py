import pytest
from src.vacancy import Vacancy

@pytest.fixture
def test_vacancy():
    return Vacancy(
        name="Test Vacancy",
        requirements="Python, Django",
        url="https://test.com/vacancy/1",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        employer="Test Company"
    )

@pytest.fixture
def test_vacancies():
    return [
        Vacancy(
            name="Python Developer",
            requirements="Python, Django",
            url="https://test.com/vacancy/1",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            employer="Company A"
        ),
        Vacancy(
            name="Java Developer",
            requirements="Java, Spring",
            url="https://test.com/vacancy/2",
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            employer="Company B"
        )
    ]