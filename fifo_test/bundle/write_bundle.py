from toffee import Bundle, Signals


class WriteBundle(Bundle):
    we_i, data_i = Signals(2)

    def enqueue(self, data):
        self.we_i.value = 1
        self.data_i.value = data
        self.step(1)

        self.we_i.value = 0
        self.step(1)
