from nlxpy.misc.unitransmit import UniTransmit as uni
import time


class Ctx:
    def __init__(self, name):
        self.name = name
        self.count = 0


def on_rx_callback(instance, context):
    context.count += 1
    print(context.name, context.count)


if __name__ == "__main__":
    ut1 = uni(
        interface="udp",
        on_recv=on_rx_callback,
        context=Ctx("ut1"),
        local_addr=("0.0.0.0", 5005),
        remote_addr=("127.0.0.1", 5006),
    )
    ut2 = uni(
        interface="udp",
        on_recv=on_rx_callback,
        context=Ctx("ut2"),
        local_addr=("0.0.0.0", 5006),
        remote_addr=("127.0.0.1", 5005),
    )

    ut1.write(b"ut1")
    time.sleep(1)
    ut2.write(b"ut2")
    time.sleep(1)
    # ut1.read_all()
    # ut2.read_all()
