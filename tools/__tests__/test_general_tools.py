from tools.general_tools import DummyTool


def test_dummy_tool():
    tool = DummyTool()
    question = "Any question"
    expected_result = "Pass to the final answer\n"
    assert tool._run(question) == expected_result
