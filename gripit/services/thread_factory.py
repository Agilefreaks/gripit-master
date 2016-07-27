from threading import Thread


class ThreadFactory:
    def create(callback):
        return Thread(target=callback)
