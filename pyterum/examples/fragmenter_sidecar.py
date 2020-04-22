import time
import socket as sock
import os
import sys

from pyterum import transmit, env
from pyterum.kill_message import KillMessage


def sender(conn):
    i = 0
    while True:
        if i > 5:
            transmit.send_to(conn, KillMessage().to_json())
            break
        msg = [f"file_no{x}.txt" for x in range(i)]
        print(f"Fragmenter Sidecar sending: '{msg}'")
        transmit.send_to(conn, msg)
        i += 1
        time.sleep(2)

def receiver(conn):
    while True:
        msg = transmit.receive_from(conn)
        print(f"Fragmenter Sidecar received: '{msg}'")

def remove_old_sockets(address:str):
    directory = os.path.dirname(address)
    try:
        os.remove(address)
    except Exception:
        pass
    try:
        os.removedirs(directory)
    except Exception:
        pass
    try:
        os.makedirs(directory)
    except Exception:
        pass


def server(address:str, as_sender:bool=True):
    while True:
        socket = sock.socket(sock.AF_UNIX)
        try:
            remove_old_sockets(address)
            socket.bind(address)
            socket.listen()
            while True:
                try:
                    print(f"Waiting for connections...", flush=True)
                    conn, _ = socket.accept()
                    print(f"Connected!", flush=True)
                    if as_sender:
                        sender(conn)
                    else:
                        receiver(conn)
                except Exception as err:
                    print(f"Fragmenter Sidecar got an exception: {err}", flush=True)
                finally:
                    conn.shutdown(sock.SHUT_RDWR)
                    conn.close()
        except Exception as err:
            print(f"Fragmenter Sidecar got an exception: {err}", flush=True)
            time.sleep(5)
        finally: 
            # Clean up before trying again. Letting the other side know we quit this connection
            socket.shutdown(sock.SHUT_RDWR)
            socket.close()

if __name__ == "__main__":
    args = sys.argv
    target_n_args = 2
    if len(args) != target_n_args:
        print(f"Wrong amount of arguments: {len(args)-1}, should be {target_n_args-1}")
        exit(1)

    as_sender = args[1].lower() != "false"

    print("Running fragmenter-sidecar example:", flush=True)
    print("Run two more instance of python as follows:", flush=True)
    print("  `python -m pyterum.examples.fragmenter`", flush=True)
    print(f"  `python -m pyterum.examples.fragmenter_sidecar {not as_sender}`", flush=True)
    if as_sender:
        server(env.EXAMPLE_SOCKET_INPUT, as_sender)
    else:
        server(env.EXAMPLE_SOCKET_OUTPUT, as_sender)