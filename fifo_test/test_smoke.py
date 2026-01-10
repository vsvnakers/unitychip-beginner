from dut import create_dut
from agent import FIFOAgent


def test_smoke_agent():
    dut = create_dut()
    agent = FIFOAgent(dut)

    assert agent.is_empty()

    agent.write_one(1)
    val = agent.read_one()
    assert val == 1

    agent.write_one(42)
    val = agent.read_one()
    assert val == 42

    assert agent.is_empty()
