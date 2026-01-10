from SyncFIFO import example


def create_dut():
    dut = example.DUTSyncFIFO()

    # reset
    dut.rst_n.value = 0
    dut.we_i.value = 0
    dut.re_i.value = 0
    dut.Step(5)

    dut.rst_n.value = 1
    dut.Step(5)

    return dut
