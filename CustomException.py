class apierror(Exception):
    def __init__(self, message="넥슨 api 오류"):
        self.message = message
        super().__init__(self.message)
