from socket import socket
import struct
import json

from pyterum import env

# The module equivalent to the one found in the iterum-go repository.
# This module implements the communication protocol between sidecar and user-defined container.
# Each message is prepended by a 4 byte unsigned integer describing its total size.
# Following that, the message is read 2048 bytes at a time until it is fully consumed

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


def _encode_msg(content) -> bytes:
    return _encode_bytes(json.dumps(content).encode("utf-8"))


def send_to(sock: socket, data):
    encoded = _encode_msg(data)
    sock.send(encoded)


def receive_from(sock: socket):
    return _decode_msg(sock)
