import pytest

from app.services.mandi import parse_agmarknet_response


def test_parses_price_mandi_name_and_date():
    raw = {
        "records": [
            {
                "commodity": "Cotton",
                "market": "Guntur",
                "modal_price": "6850",
                "arrival_date": "29/08/2026",
            }
        ]
    }

    result = parse_agmarknet_response(raw)

    assert result["price_per_quintal"] == 6850.0
    assert result["mandi_name"] == "Guntur"
    assert result["date"] == "29/08/2026"


def test_uses_first_record_when_multiple_present():
    raw = {
        "records": [
            {"commodity": "Cotton", "market": "Guntur", "modal_price": "6850",
             "arrival_date": "29/08/2026"},
            {"commodity": "Cotton", "market": "Adoni", "modal_price": "6700",
             "arrival_date": "29/08/2026"},
        ]
    }

    result = parse_agmarknet_response(raw)
    assert result["mandi_name"] == "Guntur"


def test_raises_value_error_when_no_records_found():
    raw = {"records": []}

    with pytest.raises(ValueError):
        parse_agmarknet_response(raw)
