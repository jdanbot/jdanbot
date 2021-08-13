from dataclasses import dataclass


@dataclass
class FakeBot:
    token: str = ""
    is_pin: bool = False

    async def send_message(*args, **kwargs):
        return FakeMessage()

    async def pin_chat_message(self, *args, **kwargs):
        pass


@dataclass
class FakeChat:
    id: int = 1488


@dataclass
class FakeUser:
    id: int = 1024
    full_name: str = "Unknown"


@dataclass
class FakeMessage:
    message_id: int = 246
    from_user: FakeUser = FakeUser()
    chat: FakeChat = FakeChat()


@dataclass
class FakeDispatcher:
    bot: FakeBot = FakeBot()

    class middleware:
        def setup(*args, **kwargs):
            pass

    def fake_decor_with_params(*args, **kwargs):
        def params_wrapper(*args, **kwargs):
            def wrapper(*args, **kwargs):
                pass

            return wrapper

        return params_wrapper

    message_handler = fake_decor_with_params
    callback_query_handler = fake_decor_with_params
    errors_handler = fake_decor_with_params
