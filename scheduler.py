from redis import StrictRedis
from google.cloud import pubsub_v1

from yajl import dumps
from time import sleep
from queue import Queue

from config import Config


class Scheduler:
    def __init__(self, jq_name: str, wq_name: str):
        """
        Initaies the schedules
        :param jq_name: Job Queue name
        :param wq_name: Worker Queue name
        """
        self.job_queue_name = jq_name
        self.worker_queue_name = wq_name
        self.worker_queue = Queue()
        self.job_queue = Queue()
        self.thread = None
        self.project = Config.get("project_name", "dfunc-bu")
        self.publisher = pubsub_v1.PublisherClient()

    def __publish(self, worker, job):
        """
        Publish to worker
        :param worker: worker ID
        :param job: Job ID
        """
        worker = worker.encode('utf-8')
        job = job.encode('utf-8')
        topic_path = self.publisher.topic_path(self.project, worker)
        self.publisher.publish(topic_path, job)

    def handler(self, data):
        """
        Handle jobs and workers
        :param data:
        """
        msg = dumps(data)
        channel = str(msg["channel"]).encode("utf-8")
        # print(msg)
        if channel == self.worker_queue_name:
            self.worker_queue.put(msg["data"])
        elif channel == self.job_queue_name:
            self.job_queue.put(msg["data"])
        while not (self.worker_queue.empty() and self.job_queue.empty()):
            worker = self.worker_queue.get()
            job = self.job_queue.get()
            self.__publish(worker, job)

    def start_threads(self):
        """
        Starts scheduler threads
        :return:
        """
        redis_client = StrictRedis()
        pub = redis_client.pubsub()
        pub.subscribe(**{
            self.job_queue_name: self.handler,
            self.worker_queue_name: self.handler
        })
        self.thread = pub.run_in_thread(sleep_time=0.001)

    def stop(self):
        self.thread.stop()


def main():
    """
    Main function
    """
    scheduler = Scheduler("main_job_queue", "workers")
    print("Starting scheduler threads")
    scheduler.start_threads()
    try:
        print("Starting Event loop")
        while True:
            sleep(100)
    except KeyboardInterrupt:
        print("Shutting down")
        scheduler.stop()


if __name__ == "__main__":
    main()
