from app import find_service


def test_housing_plain_english():
    result = find_service("my landlord wants me out")
    assert result["matched"] is True
    assert result["service"]["id"] == "homelessness-prevention"


def test_council_tax():
    result = find_service("I cannot pay my council tax")
    assert result["matched"] is True
    assert result["service"]["id"] == "council-tax-support"


def test_ukrainian_housing_query():
    result = find_service("мені потрібна допомога з житлом")
    assert result["matched"] is True
    assert result["service"]["id"] == "homelessness-prevention"


def test_polish_financial_query():
    result = find_service("potrzebuję pomocy finansowej")
    assert result["matched"] is True
    assert result["service"]["id"] == "benefits-support"


def test_unknown_query_fails_safely():
    result = find_service("I want to renew my passport")
    assert result["matched"] is False


def test_result_always_has_official_source():
    result = find_service("missed bin collection")
    assert result["matched"] is True
    assert result["service"]["source_url"].startswith("https://")
