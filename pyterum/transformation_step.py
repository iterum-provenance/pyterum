from typing import List

from pyterum.socket_conn import SocketConn
from pyterum.local_fragment_desc import LocalFragmentDesc
from pyterum.kill_message import KillMessage
from pyterum import env
from pyterum.logger import logger

class TransformationStepInput(SocketConn):

    def __init__(self, address:str=None):
        if address == None:
            env.verify_transformation_step_envs()
            address = env.TRANSFORMATION_STEP_INPUT
        super().__init__(address, retry_policy={"consume": -1})

        logger.info(f"Initializing TransformationStepInput...")
        self.connect()
        self.produce = None
        self._consumer = super().consumer()

    # Yields None if the message is the kill message, indicating that there will be no more messages
    def consumer(self) -> LocalFragmentDesc:
        while True:
            msg = next(self._consumer)
            output = None
            try:
                output = LocalFragmentDesc.from_json(msg)
            except (KeyError, TypeError) as errFrag:
                try:
                    KillMessage.from_json(msg)
                except (KeyError, TypeError) as errKill:
                    logger.debug(errFrag)
                    logger.debug(errKill)
                    raise Exception("Could not parse message as LocalFragmentDesc nor as KillMessage")
                
            yield output


class TransformationStepOutput(SocketConn):

    def __init__(self, address:str=None):
        if address == None:
            env.verify_transformation_step_envs()
            address = env.TRANSFORMATION_STEP_OUTPUT
        super().__init__(address, retry_policy={"produce": 0})

        logger.info(f"Initializing TransformationStepOutput...")
        self.connect()
        self.consumer = None

    def produce(self, data:LocalFragmentDesc):
        super().produce(data.to_json())

    # To send that the fragmenter is done
    def produce_done(self):
        super().produce(KillMessage().to_json())