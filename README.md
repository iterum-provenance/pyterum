# Pyterum - The Python Iterum client

This is a client package used for integrating with the Iterum data provenance framework found [here](http://github.com/iterum-provenance).
It is a specific language library, for all others see [this link](https://github.com/iterum-provenance/libraries). For a generalized introduction
to the Iterum Provenance Tracking platform see the main repository over [here](https://github.com/iterum-provenance/iterum).

---

The most important parts are found in `fragmenter.py`, `transformation_step.py`, `local_fragment_desc.py`, `env.py`, and `config.py`. These files contain the core elements that Iterum builds on and abstracts them away for a user. `fragmenter.py` and `transformation_step.py` implement structures that consume and publish from and to the sidecar. This allows users to use simple for loops when writing their transformations. The file `config.py` defines how, where and when config files and data become available. `local_fragment_desc.py` contains the main structure format that message from the sidecar arrive in and should be send to. Finally, `env.py` contains some interesting, useful or even necessary environment variables that can be expected to be set when the transformation is deployed.

Below is an example of just how small and elegant a Fragmenter can be written, this fragments each file as its own fragment. Which is a usecase you come across often.

```python
from pyterum.fragmenter import FragmenterInput, FragmenterOutput
import pyterum
from pyterum import LocalFileDesc

if __name__ == "__main__":
    # Setup
    fragmenter_in = FragmenterInput()
    fragmenter_out = FragmenterOutput()

    # For each message inbound from the sidecar
    for input_msg in fragmenter_in.consumer():
        # If it is the kill message, finalize the process here
        if input_msg == None:
            print(f"Fragmenter received kill message, stopping...", flush=True)
            fragmenter_out.produce_done()
            fragmenter_out.close()
            break

        # Print some general information and make some assertions
        print(f"Fragmenter received input message", flush=True)
        print(f"\tInput contained:", flush=True)
        print(f"\t\t{len(input_msg.data_files)} data files", flush=True)

        # Produce fragments the actual message
        for filename in input_msg.data_files:
            frag = {"files": [filename], "metadata": {}}
            fragmenter_out.produce(frag)
```