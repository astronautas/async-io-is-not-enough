"""
func fakeCPUOperation(iterations int) {
	result := 0.0

	for i := 0; i < iterations; i++ {
		result += math.Sqrt(12345.6789) // Perform a CPU-intensive operation
	}
}
"""
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import click
import time
import os
import aiohttp
import asyncio

def fake_cpu_operation(iterations: int):
    result = 0.0
    noise = random.random()

    for i in range(iterations):
        result += (12345.6789 * noise ) ** 0.5 # Perform a CPU-intensive operation

# https://pymotw.com/3/asyncio/coroutines.html
async def fake_cpu_operation_async(iterations: int):
    result = 0.0
    noise = random.random()

    for i in range(iterations):
        result += (12345.6789 * noise ) ** 0.5 # Perform a CPU-intensive operation
        yield result

async def fake_cpu_operation_async_wrapper():
    async for result in fake_cpu_operation_async(10):
        print(result)

    
def fake_io_operation(seconds: int):
    # https://httpbin.org/delay/1
    import requests
    response = requests.get(f"https://httpbin.org/delay/{seconds}")
    return response.json()

async def fake_io_operation_async(seconds: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://httpbin.org/delay/{seconds}") as response:
            return await response.json()

def do_work(cpu_op_iterations: int, io_op_seconds: int):
    fake_cpu_operation(cpu_op_iterations)
    fake_io_operation(seconds=io_op_seconds)

@click.command()
@click.option("--serial", is_flag=True, help="Run tasks serially", default=False)
@click.option("--io", is_flag=True, help="IO dominated experiment, otherwise CPU", default=False)
@click.option("--with-async", is_flag=True, help="Run tasks asynchronously", default=False)
def main(serial: bool, io: bool, with_async: bool):
    # Number of threads to run the CPU-intensive operation
    num_threads = 1 if serial else os.cpu_count()
    num_experiments = 12
    CPU_OP_ITERATIONS_1SEC = 15_000_000 # 1s
    io_op_seconds = 1
    
    if io:
        if with_async:
            import asyncio
            for num_experiments in [1, 2, 4, 8, 16, 32]:
                print(f"Tasks: {num_experiments}, running with {CPU_OP_ITERATIONS_1SEC} CPU iterations and {io_op_seconds} IO seconds.")
                print(f"Number of threads: {num_threads}, Python GIL: {os.environ.get('PYTHON_GIL')}")

                async def tasks():
                    await asyncio.gather(*[fake_io_operation_async(io_op_seconds) for _ in range(num_experiments)])

                start_time = time.time()
                asyncio.run(tasks())
                end_time = time.time()
                print("Time taken: ", end_time - start_time)
        else:
            for num_experiments in [1, 2, 4, 8, 16, 32]:
                print(f"Tasks: {num_experiments}, running with {CPU_OP_ITERATIONS_1SEC} CPU iterations and {io_op_seconds} IO seconds.")
                print(f"Number of threads: {num_threads}, Python GIL: {os.environ.get('PYTHON_GIL')}")

                # Create a pool of threads
                with ThreadPoolExecutor(max_workers=num_threads) as pool:
                    start_time = time.time()

                    futures = [
                        pool.submit(do_work, 1, io_op_seconds) # negligible CPU operation
                        for _ in range(num_experiments)
                    ]

                    # Wait for all tasks to complete
                    for future in as_completed(futures):
                        # Optionally, handle results or exceptions
                        try:
                            future.result()  # Raises any exception from the task
                        except Exception as e:
                            print(f"Task failed with exception: {e}")
                        
                end_time = time.time()
                print("Time taken: ", end_time - start_time)
    else:
        for num_experiments in [1, 2, 4, 8, 16, 32]:
            print(f"Tasks: {num_experiments}, running with {CPU_OP_ITERATIONS_1SEC} CPU iterations and {io_op_seconds} IO seconds.")
            print(f"Number of threads: {num_threads}, Python GIL: {os.environ.get('PYTHON_GIL')}")

            # Create a pool of threads
            with ThreadPoolExecutor(max_workers=num_threads) as pool:
                start_time = time.time()

                futures = [
                    pool.submit(do_work, CPU_OP_ITERATIONS_1SEC, 1) # negligible IO operation
                    for _ in range(num_experiments)
                ]

                # Wait for all tasks to complete
                for future in as_completed(futures):
                    # Optionally, handle results or exceptions
                    try:
                        future.result()  # Raises any exception from the task
                    except Exception as e:
                        print(f"Task failed with exception: {e}")
                    
            end_time = time.time()
            print("Time taken: ", end_time - start_time)
    
        # async def tasks():
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get("https://httpbin.org/delay/1") as response:
        #             print(await response.json())

        # for num_experiments in [1, 2, 4, 8, 16, 32]:
        #     print(f"Tasks: {num_experiments}, running with {cpu_op_iterations} CPU iterations and {io_op_seconds} IO seconds.")
        #     print(f"Number of threads: {num_threads}, Python GIL: {os.environ.get('PYTHON_GIL')}")

        # import aiohttp
        # import asyncio

        # asyncio.run(tasks())


            # # Create a pool of threads
            # with ThreadPoolExecutor(max_workers=num_threads) as pool:
            #     start_time = time.time()

            #     futures = [
            #         pool.submit(do_work, cpu_op_iterations, 1) # negligible IO operation
            #         for _ in range(num_experiments)
            #     ]

            #     # Wait for all tasks to complete
            #     for future in as_completed(futures):
            #         # Optionally, handle results or exceptions
            #         try:
            #             future.result()  # Raises any exception from the task
            #         except Exception as e:
            #             print(f"Task failed with exception: {e}")
                    
            # end_time = time.time()
            # print("Time taken: ", end_time - start_time)
            
    # if io:
    #     experiments = [(1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)]
    # else:
    #     experiments = [(1_000_000, 1), (2_000_000, 1), (4_000_000, 1), (8_000_000, 1), (16_000_000, 1), (32_000_000, 1)]

    # for cpu_op_iters, io_op_secs in [(1_000_000, 1), (2_000_000, 1), (4_000_000, 1), (8_000_000, 1), (16_000_000, 1), (32_000_000, 1)]:
    #     print(f"Tasks: {num_experiments}, running with {cpu_op_iters} CPU iterations and {io_op_secs} IO seconds.")
    #     print(f"Number of threads: {num_threads}, Python GIL: {os.environ.get('PYTHON_GIL')}")

    #     # Create a pool of threads
    #     with ThreadPoolExecutor(max_workers=num_threads) as pool:
    #         start_time = time.time()

    #         futures = [
    #             pool.submit(do_work, cpu_op_iters, io_op_secs)
    #             for _ in range(num_experiments)
    #         ]

    #         # Wait for all tasks to complete
    #         for future in as_completed(futures):
    #             # Optionally, handle results or exceptions
    #             try:
    #                 future.result()  # Raises any exception from the task
    #             except Exception as e:
    #                 print(f"Task failed with exception: {e}")
                
    #     end_time = time.time()
    #     print("Time taken: ", end_time - start_time)

    # So, as expected, with threadpool, the time taken is less than the time taken with the processpool

if __name__ == '__main__':
    main()