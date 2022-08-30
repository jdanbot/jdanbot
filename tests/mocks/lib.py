def append_to_replies(func):
    async def wrapper(self, *args, **kwargs):
        msg = await func(self, *args, **kwargs)
        self.replies.append(msg)

        return msg

    return wrapper
