class CustomException(Exception):
    def __init__(self, message):
        self.message = message

async def handle_custom_exception(exception: CustomException):
    return {"error": exception.message}
