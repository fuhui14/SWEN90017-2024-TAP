from concurrent.futures import ThreadPoolExecutor

# this is a thread pool executor with a maximum of 3 workers
executor = ThreadPoolExecutor(max_workers=3)