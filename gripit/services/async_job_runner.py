from gripit.services.reader import Reader
from gripit.services.thread_factory import ThreadFactory
from gripit.config import Config


class AsyncJobRunner:
    def __init__(self):
        self.__running_jobs = []

    def start(self, job):
        thread = ThreadFactory.create(job.run)
        thread.start()

        self.__running_jobs.append(dict({'thread': thread, 'job': job}))

    def stop(self, job):
        entry = next((
            entry for entry in self.__running_jobs
            if entry['job'] == job and entry['thread'].is_alive()
        ), None)

        if not entry == None:
            entry['job'].stop()
            entry['thread'].join()

    def is_idle(self):
        running_entry = next((entry for entry in self.__running_jobs if entry['thread'].is_alive()), None)

        return running_entry == None
