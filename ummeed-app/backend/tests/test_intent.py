from app.services.intent import detect_intent


def test_detects_weather_intent_from_spray_question():
    result = detect_intent("Should I spray my cotton today or wait for the rain?")
    assert result["needs_weather"] is True
    assert result["needs_mandi_price"] is False


def test_detects_mandi_price_intent_from_selling_question():
    result = detect_intent("Should I sell my paddy now or wait a week?")
    assert result["needs_mandi_price"] is True
    assert result["needs_weather"] is False


def test_detects_both_when_question_touches_both():
    result = detect_intent("Will the rain affect cotton prices this week?")
    assert result["needs_weather"] is True
    assert result["needs_mandi_price"] is True


def test_detects_neither_for_pure_advisory_question():
    result = detect_intent("What causes yellow spots on cotton leaves?")
    assert result["needs_weather"] is False
    assert result["needs_mandi_price"] is False


def test_extracts_known_crop_name_when_present():
    result = detect_intent("What is today's price for cotton?")
    assert result["crop"] == "cotton"


def test_crop_is_none_when_no_known_crop_mentioned():
    result = detect_intent("What government schemes exist for farmers?")
    assert result["crop"] is None


def test_detection_is_case_insensitive():
    result = detect_intent("SHOULD I SELL MY COTTON NOW?")
    assert result["needs_mandi_price"] is True
    assert result["crop"] == "cotton"
