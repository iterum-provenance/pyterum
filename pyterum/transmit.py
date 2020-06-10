from socket import socket
import struct
import json

from pyterum import env


def _encode_msg_size(size: int) -> bytes:
    return struct.pack("<I", size)


def _decode_msg_size(size_bytes: bytes) -> int:
    return struct.unpack("<I", size_bytes)[0]


def _encode_bytes(content: bytes) -> bytes:
    size = len(content)
    return _encode_msg_size(size) + content


def _decode_msg(target: socket):
    enc_msg_size = target.recv(env.ENC_MSG_SIZE_LENGTH)
    msg_size = _decode_msg_size(enc_msg_size)
    chunks = []
    bytes_recd = 0
    while bytes_recd < msg_size:
        buf_size = min(msg_size - bytes_recd, 2048)
        chunk = target.recv(buf_size)
        if chunk == b'':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    enc_msg = b''.join(chunks)
    return json.loads(enc_msg)


def recv_chunked(target: socket, message_length):
    chunks = []
    bytes_recd = 0
    while bytes_recd < message_length:
        chunk = target.recv(min(message_length - bytes_recd, 2048))
        if chunk == b'':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)


def _encode_msg(content) -> bytes:
    return _encode_bytes(json.dumps(content).encode("utf-8"))


def send_to(sock: socket, data):
    encoded = _encode_msg(data)
    sock.send(encoded)


def receive_from(sock: socket):
    return _decode_msg(sock)
