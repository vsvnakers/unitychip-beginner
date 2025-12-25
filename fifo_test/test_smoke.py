# =========================
# import DUT
# =========================
try:
    from UT_SyncFIFO import *
except:
    from SyncFIFO import *


# =========================
# helper: cycle
# =========================
def cycle(dut, n=1):
    for _ in range(n):
        dut.Step(1)


# =========================
# helper: reset
# =========================
def reset_dut(dut):
    dut.we_i.value = 0
    dut.re_i.value = 0
    dut.data_i.value = 0

    dut.rst_n.value = 0
    cycle(dut, 5)

    dut.rst_n.value = 1
    cycle(dut, 1)


# =========================
# 1. reset test (default)
# =========================
def test_reset_dut_default():
    dut = DUTSyncFIFO(
        waveform_filename="reset_default.fst"
    )
    dut.InitClock("clk")

    reset_dut(dut)

    dut.Finish()
    print("Reset test (default) finished")


# =========================
# 2. reset test (imme)
# =========================
def test_reset_dut_imme():
    dut = DUTSyncFIFO(
        waveform_filename="reset_imme.fst"
    )
    dut.InitClock("clk")

    dut.rst_n.AsImmWrite()

    reset_dut(dut)

    dut.Finish()
    print("Reset test (imme) finished")


# =========================
# 3. reset + assert
# =========================
def test_reset_dut_assert():
    dut = DUTSyncFIFO(
        waveform_filename="reset_assert.fst"
    )
    dut.InitClock("clk")

    reset_dut(dut)

    # FIFO outputs
    assert dut.data_o.value == 0
    assert dut.empty_o.value == 1
    assert dut.full_o.value == 0

    # internal signals
    wptr = dut.GetInternalSignal("SyncFIFO_top.SyncFIFO.wptr")
    rptr = dut.GetInternalSignal("SyncFIFO_top.SyncFIFO.rptr")
    counter = dut.GetInternalSignal("SyncFIFO_top.SyncFIFO.counter")

    assert wptr.value == 0
    assert rptr.value == 0
    assert counter.value == 0

    dut.Finish()
    print("Reset assert test passed")


# =========================
# 4. smoke test
# =========================
def test_smoke_dut():
    dut = DUTSyncFIFO(
        waveform_filename="smoke.fst"
    )
    dut.InitClock("clk")

    # reset
    reset_dut(dut)

    # ---------- write 0x114 ----------
    dut.we_i.value = 1
    dut.data_i.value = 0x114
    cycle(dut, 1)

    dut.we_i.value = 0
    cycle(dut, 1)

    assert dut.empty_o.value == 0


    # ---------- write 0x514 ----------
    dut.we_i.value = 1
    dut.data_i.value = 0x514
    cycle(dut, 1)

    dut.we_i.value = 0
    cycle(dut, 1)


    # ---------- read 0x114 ----------
    dut.we_i.value = 0
    dut.re_i.value = 1
    cycle(dut, 1)
    cycle(dut, 1)

    assert dut.data_o.value == 0x114

    # ---------- read 0x514 ----------
    cycle(dut, 1)
    cycle(dut, 1)

    assert dut.data_o.value == 0x514
    assert dut.empty_o.value == 1

    dut.Finish()
    print("Smoke test passed!")


# =========================
# main
# =========================
if __name__ == "__main__":
    test_reset_dut_default()
    test_reset_dut_imme()
    test_reset_dut_assert()
    test_smoke_dut()
