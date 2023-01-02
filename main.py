import multiprocessing as mp
import tqdm
import functions as func


def main():
    csv_file = "E:/irq_dataset/iraq_sigacts.csv"
    # list with sigacts html files
    files_sigact = func.flat_sigact_files('irq/event')
    # headers row inside csv
    func.first_row(csv_file)
    # Manager to manage async queue
    manager = mp.Manager()
    # Queue to save jobs
    q = manager.Queue()
    # Number of workers
    pool = mp.Pool(mp.cpu_count())
    # Starting a watcher who scans the queue and writes rows to the csv file
    watcher = pool.apply_async(func.listener, (q, csv_file,))
    jobs = []
    # Progress bar where an entire file is a chunk
    with tqdm.tqdm(total=len(files_sigact)) as pbar:
        for file_name in files_sigact:
            # Async worker in every html file
            job = pool.apply_async(func.html_parser, (file_name, q))
            # Saves job object inside job list
            jobs.append(job)
        for job in jobs:
            # Retrieve data from job object
            job.get()
            # Updates progress bar
            pbar.update(1)
    # collect results from the workers through the pool result queue
        # In order to kill the watcher we put last_row as last job object
        q.put('last_row')
        # Stops multiprocessing tasks after all jobs are done
        pool.close()
        pool.join()
        # Stops progress bar
        pbar.close()


if __name__ == "__main__":
    main()
