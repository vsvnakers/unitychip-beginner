from toffee import Bundle, Signals


class ReadBundle(Bundle):
    re_i, data_o = Signals(2)

    def dequeue(self):
        self.re_i.value = 1
        self.step(1)

        self.re_i.value = 0
        self.step(1)

        return int(self.data_o.value)
