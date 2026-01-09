#!/usr/bin/env python3

import threading
import socket
import queue
import time

try:
    import serial
except ImportError:
    serial = None


class MetaTransmit:
    """
    Unified byte-stream abstraction.
    """

    def __init__(self, on_recv=None, context=None, newline=b"\n"):
        self._rx_queue = queue.Queue()
        self._buffer = bytearray()
        self._running = False
        self._thread = None
        self._newline = newline
        self._on_recv = on_recv
        self._context = context

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()

    def _recv_loop(self):
        raise NotImplementedError

    def close(self):
        self._running = False

    def _fill_buffer(self, block=True, timeout=None):
        try:
            data = self._rx_queue.get(block=block, timeout=timeout)
            self._buffer.extend(data)
            # if self._on_recv:
            #     try:
            #         self._on_recv(self, self._context)
            #     except Exception as e:
            #         print(f"[unitransmit] on_rx callback error: {e}")
            return True
        except queue.Empty:
            return False

    def _enqueue_and_notify(self, data: bytes):
        self._buffer.extend(data)
        if self._on_recv:
            try:
                self._on_recv(self, self._context)
            except Exception as e:
                print(f"[unitransmit] on_recv callback error: {e}")

    def _inject_rx(self, data: bytes):
        """Inject received data into buffer and trigger callback"""
        self._buffer.extend(data)
        if self._on_recv:
            try:
                self._on_recv(self, self._context)
            except Exception as e:
                print(f"[unitransmit] on_recv callback error: {e}")

    def read(self, size: int = 1) -> bytes:
        """
        Blocking read exactly `size` bytes.
        """
        while len(self._buffer) < size:
            if not self._fill_buffer(block=True):
                break

        data = self._buffer[:size]
        del self._buffer[:size]
        return bytes(data)

    def read_all(self) -> bytes:
        """
        Non-blocking read of all available data.
        """
        while self._fill_buffer(block=False):
            pass

        data = bytes(self._buffer)
        self._buffer.clear()
        return data

    def readln(self) -> bytes:
        """
        Read until newline.
        """
        while True:
            idx = self._buffer.find(self._newline)
            if idx != -1:
                end = idx + len(self._newline)
                data = self._buffer[:end]
                del self._buffer[:end]
                return bytes(data)

            self._fill_buffer(block=True)

    def write(self, data: bytes):
        raise NotImplementedError

    def writeln(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.write(data + self._newline)


class LoopbackTransmit(MetaTransmit):
    """
    Loopback / in-process transmit.
    write() -> read()
    """

    def __init__(self, **kw):
        super().__init__(**kw)
        # 不需要 start / recv_loop

    def write(self, data: bytes):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        self._inject_rx(bytes(data))

    def close(self):
        self._running = False


class SerialTransmit(MetaTransmit):
    def __init__(self, port, baudrate=115200, timeout=0.1, **kw):
        if serial is None:
            raise RuntimeError("pyserial not installed")

        super().__init__(**kw)
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.start()

    def _recv_loop(self):
        while self._running:
            if self.ser.in_waiting:
                data = self.ser.read(self.ser.in_waiting)
                # self._rx_queue.put(data)
                self._enqueue_and_notify(data)
            time.sleep(0.01)

    def write(self, data: bytes):
        self.ser.write(data)

    def close(self):
        super().close()
        self.ser.close()


class UDPTransmit(MetaTransmit):
    def __init__(self, local_addr, remote_addr=None, **kw):
        super().__init__(**kw)
        self.remote_addr = remote_addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(local_addr)
        self.sock.settimeout(0.2)
        self.start()

    def _recv_loop(self):
        while self._running:
            try:
                data, _ = self.sock.recvfrom(65535)
                # self._rx_queue.put(data)
                self._enqueue_and_notify(data)
            except socket.timeout:
                continue

    def write(self, data: bytes, addr=None):
        target = addr or self.remote_addr
        if not target:
            raise ValueError("UDP remote address not set")
        self.sock.sendto(data, target)

    def close(self):
        super().close()
        self.sock.close()


class TCPTransmit(MetaTransmit):
    def __init__(self, host, port, role="client", **kw):
        super().__init__(**kw)
        self.role = role

        if role == "server":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((host, port))
            self.sock.listen(1)
            self.conn, _ = self.sock.accept()
        else:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((host, port))

        self.conn.settimeout(0.2)
        self.start()

    def _recv_loop(self):
        while self._running:
            try:
                data = self.conn.recv(4096)
                if not data:
                    break
                # self._rx_queue.put(data)
                self._enqueue_and_notify(data)
            except socket.timeout:
                continue

    def write(self, data: bytes):
        self.conn.sendall(data)

    def close(self):
        super().close()
        self.conn.close()


class UniTransmit:
    """
    User-facing unified interface.
    """

    def __init__(self, interface: str, on_recv=None, context=None, **kwargs):
        interface = interface.lower()

        if interface in ("loop", "loopback"):
            self._impl = LoopbackTransmit(on_recv=on_recv, context=context, **kwargs)
        elif interface == "serial":
            self._impl = SerialTransmit(on_recv=on_recv, context=context, **kwargs)
        elif interface == "udp":
            self._impl = UDPTransmit(on_recv=on_recv, context=context, **kwargs)
        elif interface == "tcp":
            self._impl = TCPTransmit(on_recv=on_recv, context=context, **kwargs)
        else:
            raise ValueError(f"Unsupported interface: {interface}")

    def read(self, size: int = 1) -> bytes:
        return self._impl.read(size)

    def read_all(self) -> bytes:
        return self._impl.read_all()

    def readln(self) -> bytes:
        return self._impl.readln()

    def write(self, data: bytes):
        return self._impl.write(data)

    def writeln(self, data):
        return self._impl.writeln(data)

    def close(self):
        self._impl.close()
