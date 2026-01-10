from toffee import Bundle, Signals


class StatusBundle(Bundle):
    full_o, empty_o = Signals(2)
