try:
    from UT_SyncFIFO import *
except:
    try:
        from SyncFIFO import *
    except:
        from __init__ import *


def cycle(dut, n=1):
    for _ in range(n):
        dut.Step(1)

# def test_reset_dut_default():
#     dut = DUTSyncFIFO(
#         waveform_filename="reset_default.fst"
#     )
#     dut.InitClock("clk")

#     dut.we_i.value = 0
#     dut.re_i.value = 0
#     dut.data_i.value = 0
#     dut.rst_n.value = 0

#     cycle(dut, 5)

#     dut.rst_n.value = 1
#     cycle(dut, 2)
#     dut.Finish()
#     print("Reset test (default mode) finished")

def test_reset_dut_imme():
    dut = DUTSyncFIFO(
        waveform_filename="reset_imme.fst"
    )
    dut.InitClock("clk")

    dut.rst_n.AsImmWrite()
    dut.we_i.value = 0
    dut.re_i.value = 0
    dut.data_i.value = 0

    dut.rst_n.value = 0
    cycle(dut, 5)

    dut.rst_n.value = 1
    cycle(dut, 2)

    dut.Finish()
    print("Reset test (imme mode) finished")

def test_reset_dut_default_assert():
    dut = DUTSyncFIFO(
        waveform_filename="reset_default_assert.fst"
    )
    dut.InitClock("clk")

    dut.we_i.value = 0
    dut.re_i.value = 0
    dut.data_i.value = 0

    dut.rst_n.value = 0
    cycle(dut, 5)

    dut.rst_n.value = 1
    cycle(dut, 1)

    assert dut.data_o.value == 0, "data_o should be 0 after reset"
    assert dut.empty_o.value == 1, "empty_o should be 1 after reset"
    assert dut.full_o.value == 0, "full_o should be 0 after reset"

    dut.Finish()
    print("Reset test (default mode) passed")





if __name__ == "__main__":
    # test_reset_dut_default_assert()
    test_reset_dut_imme()

