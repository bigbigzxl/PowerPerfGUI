from __future__ import absolute_import
from __future__ import unicode_literals
from functools import reduce
import random
import string

from mock import patch, call, MagicMock
import pytest

from adbpy.socket import Socket, int_to_hex, SocketError
from tests.mock_socket import MockSocket
from .utils import random_ascii

def test_int_to_hex():
    assert int_to_hex(2) == "0002"
    assert int_to_hex(255) == "00ff"
    assert int_to_hex(256) == "0100"
    assert int_to_hex(100) == "0064"
    assert int_to_hex(0) == "0000"

def test_int_to_hex_overflow():
    with pytest.raises(ValueError):
        int_to_hex(65536)

@pytest.fixture
def socket():
    sock = Socket(())
    sock.socket = MockSocket()
    return sock

def test_send_data_normal_response(socket):
    data_sent = [] 
    def send(message):
        data_sent.append(message.decode("ascii"))
        return len(message)

    socket.socket.send = send

    data = "host:track-devices"

    socket._send_data(data)

    assert len(data_sent) == 1
    assert data == data_sent[0]

def test_send_data_staggered_response(socket):
    data_sent = [] 
    def send(message):
        data_sent.append(message.decode("ascii")[0])
        return 1

    socket.socket.send = send
    data = "host:track-devices"

    socket._send_data(data)

    assert len(data) == len(data_sent)
    assert data == ''.join(data_sent)

def test_send_data_failed_response(socket):
    response_lengths = [0, 1]
    socket.socket.send = lambda x: response_lengths.pop()

    with pytest.raises(RuntimeError):
        socket._send_data("long test string")

def test_receive_fixed_length_full_response(socket):
    data_to_recv = "0005"

    socket.socket.recv = lambda x: data_to_recv.encode("ascii")

    data = socket.receive_fixed_length(4)
    assert data_to_recv == data

def test_receive_fixed_length_staggered_response(socket):
    data_to_recv = "0005"
    split_data = list(data_to_recv)
    split_data.reverse()

    socket.socket.recv = lambda x: split_data.pop().encode("ascii")

    data = socket.receive_fixed_length(4)
    assert data_to_recv == data

def test_receive_failed_response(socket):
    responses = ['', 'hi']
    socket.socket.recv = lambda x: responses.pop().encode("ascii")

    with pytest.raises(RuntimeError):
        socket.receive_fixed_length(100)

def test_receive_full_respose(socket):
    expected_data = 'hello_respose'
    responses = ['OKAY', '000d', expected_data]
    socket.socket.recv = lambda x: responses.pop(0).encode("ascii")

    data = socket.receive()

    assert data == expected_data

    expected_data = '950a8ad5\toffline\n6097191b\tdevice\n'
    responses = ['OKAY', int_to_hex(len(expected_data)), expected_data]

    data = socket.receive()

    assert data == expected_data

def test_receive_staggered_respose(socket):
    expected_data = '950a8ad5\toffline\n6097191b\tdevice\n'
    responses = ['OK', 'AY', int_to_hex(len(expected_data)),
            expected_data[:10], expected_data[10:]]
    socket.socket.recv = lambda x: responses.pop(0).encode("ascii")

    data = socket.receive()

    assert data == expected_data

def test_receive_fail_response(socket):
    expected_data = 'big error'
    responses = ['FA', 'IL', int_to_hex(len(expected_data)),
                 expected_data]
    socket.socket.recv = lambda x: responses.pop(0).encode("ascii")

    with pytest.raises(SocketError):
        socket.receive()

def test_receive_socket_fail_response(socket):
    expected_data = 'big error'
    responses = ['FA', 'IR']
    socket.socket.recv = lambda x: responses.pop(0).encode("ascii")

    with pytest.raises(SocketError):
        socket.receive()

def test_send(socket):
    data = "host:version"
    with patch.object(Socket, '_send_data') as send_data_method:
        socket.send(data)

        calls = [call(int_to_hex(len(data))), call(data)]
        send_data_method.assert_has_calls(calls)

def test_receive_until_end(socket):
    expected_data = random_ascii(1000)
    socket.socket.set_buffer(expected_data)

    socket.receive_fixed_length = MagicMock(return_value="OKAY")

    data = socket.receive_until_end()
    assert expected_data == data

def test_receive_until_end_fail(socket):
    expected_data = random_ascii(1000)
    socket.socket.set_buffer(expected_data)

    socket.receive_fixed_length = MagicMock(return_value="FAIL")

    with pytest.raises(SocketError):
        socket.receive_until_end()

def test_receive_until_end_timeout(socket):
    expected_data = random_ascii(10000)
    socket.socket.set_buffer(expected_data)

    socket.receive_fixed_length = MagicMock(return_value="OKAY")

    data = socket.receive_until_end(timeout=10)
    assert expected_data != data
    assert data in expected_data
