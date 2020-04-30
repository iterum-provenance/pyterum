from pyterum.fragmenter import FragmenterInput, FragmenterOutput
from pyterum import env


if __name__ == "__main__":
    print("Running fragmenter example:", flush=True)
    print("Run two more instance of python as follows:", flush=True)
    print("  `python -m pyterum.examples.fragmenter_sidecar false`", flush=True)
    print("  `python -m pyterum.examples.fragmenter_sidecar true`", flush=True)
    
    fragmenter_in = FragmenterInput(env.EXAMPLE_SOCKET_INPUT)
    fragmenter_out = FragmenterOutput(env.EXAMPLE_SOCKET_OUTPUT)
    
    for file_list in fragmenter_in.consumer():
        print(f"Fragmenter received: {file_list}", flush=True)
        if file_list == None:
            fragmenter_out.produce_done()
            fragmenter_out.close()
            break

        for f in file_list:
            msg = [f]
            print(f"Fragmenter sending: {msg}", flush=True)
            fragmenter_out.produce(msg)