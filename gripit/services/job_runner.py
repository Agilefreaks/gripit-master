from gripit.services.thread_factory import ThreadFactory


class JobRunner:
    def __init__(self):
        self.__current_job = None

    def start(self, job):
        if not self.is_idle():
            raise Exception('A job was already running')
        thread = ThreadFactory.create(job.run)
        thread.start()
        self.__current_job = job

    def stop(self):
        if self.__current_job is not None:
            self.__current_job.stop()

    def is_idle(self):
        return self.__current_job is None

    def is_busy(self):
        return not self.is_idle()
