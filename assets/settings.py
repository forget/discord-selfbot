class Config(object):
    def __init__(self) -> None:
        self.token: str = "" # your authorization token
        
        self.accept_friend_requests: bool = True
        self.send_message: bool = True
        self.delay_accept: bool = False
        self.delay_message: bool = False
        self.delete_after_execution: bool = True
        
        self.message: str = ":zzz: I am away..."
        self.accept_delay: int = 1
        self.message_delay: int = 1
