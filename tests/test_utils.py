from ai_creature_generator.utils import extract_html_code, remove_think_tags, simple_parse_qs


class TestExtractHtmlCode:
    def test_extracts_html_block(self):
        text = "some text ```html\n<div>hello</div>\n``` more"
        assert extract_html_code(text) == "<div>hello</div>"

    def test_returns_raw_text_when_no_markers(self):
        text = "<div>plain</div>"
        assert extract_html_code(text) == "<div>plain</div>"

    def test_handles_empty_string(self):
        assert extract_html_code("") == ""


class TestRemoveThinkTags:
    def test_removes_think_block(self):
        text = "<think>some reasoning</think>output here"
        assert remove_think_tags(text) == "output here"

    def test_no_think_tag_returns_original(self):
        text = "just output"
        assert remove_think_tags(text) == "just output"

    def test_handles_empty_string(self):
        assert remove_think_tags("") == ""


class TestSimpleParseQs:
    def test_parses_simple_query(self):
        result = simple_parse_qs(b"email=test@test.de&password=secret")
        assert result["email"] == "test@test.de"
        assert result["password"] == "secret"

    def test_handles_empty_bytes(self):
        assert simple_parse_qs(b"") == {}

    def test_decodes_url_encoding(self):
        result = simple_parse_qs(b"key=hello%20world")
        assert result["key"] == "hello world"
