import concurrent.futures
import logging
import threading
import time  # very strange bug, if not import, run Okay, not throw exception


class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        # with self._lock:
        #     logging.debug("Thread %s has lock", name)
        #     local_copy = self.value
        #     local_copy += 1
        #     time.sleep(0.1)
        #     self.value = local_copy
        #     logging.debug("Thread %s about to release lock", name)
 
        l = self._lock
        l.acquire()  # manually call acquire and release

        logging.debug("Thread %s has lock", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.debug("Thread %s about to release lock", name)

        l.release()
 
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    database = FakeDatabase()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.locked_update, index)

    #x = threading.Thread(target=database.update, args=(1, ))
    #x.start()

    #y = threading.Thread(target=database.update, args=(2, ))
    #y.start()

    #x.join()
    #y.join()

    logging.info("Testing update. Ending value is %d.", database.value)
