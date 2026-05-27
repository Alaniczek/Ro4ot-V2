import asyncio


class ResponseProtocol(asyncio.DatagramProtocol):
    def __init__(self, handler):
        self.handler = handler

    def datagram_received(self, data, addr):
        print(f"\n[UDP IN] Packet from {addr}")
        try:
            message = data.decode('utf-8').strip()
            print(f"[UDP IN] Content: '{message}'")

            if self.handler.on_message_callback:
                loop = asyncio.get_running_loop()
                task = loop.create_task(self.handler.on_message_callback(addr[0], message))
                self.handler._background_tasks.add(task)
                task.add_done_callback(self.handler._background_tasks.discard)

        except Exception as e:
            print(f"[UDP ERR] Error decoding packet from {addr}: {e}")


class ResponseHandler:
    def __init__(self, robot_manager):
        self.robot_manager = robot_manager
        self.on_message_callback = None
        self.transport = None
        self._background_tasks = set()

    async def start(self, port=17145):
        loop = asyncio.get_running_loop()
        try:
            self.transport, protocol = await loop.create_datagram_endpoint(
                lambda: ResponseProtocol(self),
                local_addr=('0.0.0.0', port)
            )
            print(f"[UDP] Listening for responses on PORT {port} (0.0.0.0)")
            return self.transport
        except Exception as e:
            print(f"[UDP ERR] Could not start UDP listener on port {port}: {e}")
            raise e

    def set_callback(self, callback):
        self.on_message_callback = callback

    def stop(self):
        if self.transport:
            self.transport.close()
            print("[UDP] Listener stopped.")