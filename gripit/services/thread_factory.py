from threading import Thread


class ThreadFactory:
    @staticmethod
    def create(callback):
        return Thread(target=callback)
