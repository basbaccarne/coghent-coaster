"""
This is the main CoGhent Coaster script
It uses python's multiprocessing to manage the difference components of the application
- fetch gets new data from the server
- interface shows and interacts with the user
"""
import multiprocessing


def get_new_images():
    import src.fetcher


def launch_interface():
    import src.interface


if __name__ == "__main__":
    process1 = multiprocessing.Process(target=get_new_images)
    process2 = multiprocessing.Process(target=launch_interface)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
