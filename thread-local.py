import logging
import threading
import time


def thread_function(name, mydata):
    logging.info("Thread %s: starting", name)
    mydata.x = name
    time.sleep(2)
    logging.info("Thread %s: mydata is %d", name, mydata.x)
    logging.info(f"Mydata is {mydata}")
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    mydata = threading.local()

    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,mydata))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
