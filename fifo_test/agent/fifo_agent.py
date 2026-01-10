from bundle import WriteBundle, ReadBundle, StatusBundle


class FIFOAgent:
    def __init__(self, dut):
        self.dut = dut

        self.write = WriteBundle()
        self.read = ReadBundle()
        self.status = StatusBundle()

        self.write.bind(dut)
        self.read.bind(dut)
        self.status.bind(dut)

        # ⭐ 关键：reset 后，等 FIFO empty_o 真的拉高
        self._wait_empty_after_reset()

    def _wait_empty_after_reset(self):
        # 最多等 100 个 cycle，防止死循环
        for _ in range(100):
            if int(self.status.empty_o.value) == 1:
                return
            self.dut.Step(1)

        raise RuntimeError("FIFO did not become empty after reset")

    def write_one(self, data):
        self.write.enqueue(data)

    def read_one(self):
        return self.read.dequeue()

    def is_empty(self):
        return int(self.status.empty_o.value) == 1

    def is_full(self):
        return int(self.status.full_o.value) == 1
