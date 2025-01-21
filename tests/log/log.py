class FunLog:
    def __init__(self, prefix=""):
        self.prefix = prefix
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"{self.prefix} '{func.__name__}' 함수가 호출되었습니다.")
            return func(*args, **kwargs)
        return wrapper

