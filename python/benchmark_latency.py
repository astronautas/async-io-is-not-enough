import requests
import time
import random
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

def preprocess_feature_batch(iterations: int):
    '''
    This is a fake CPU operation that is used to simulate a CPU-intensive operation.
    Some realistic potential cases:
    '''
    def fake_cpu_op(iterations: int):
        result = 0.0
        noise = random.random()

        for i in range(iterations):
            result += (12345.6789 * noise ) ** 0.5 # Perform a CPU-intensive operation

    fake_cpu_op(iterations)
    
async def get_feature_batch():
    async with aiohttp.ClientSession() as session:
        # ~0.5s on MCB Pro M1
        async with session.get(f"https://httpbin.org/delay/1") as response:
            return await response.json()

async def prepare_feature_batch(preprocessing: bool = False, fraction_of_io: float = 0.0):
    features = await get_feature_batch()

    if preprocessing and fraction_of_io > 0.0:
        loop = asyncio.get_event_loop()

        # 15_000_000 ~= 2.3s on MCB Pro M1
        # a good practice to use run_in_executor to run CPU-bound non-async tasks to not block the event loop
        await loop.run_in_executor(None, preprocess_feature_batch, int(fraction_of_io * 15_000_000 / 0.8 * 2))

def prepare_feature_batch_serial(preprocessing: bool = False, fraction_of_io: float = 0.0):
    features = requests.get(f"https://httpbin.org/delay/1").json()

    if preprocessing and fraction_of_io > 0.0:
        preprocess_feature_batch(int(fraction_of_io * 15_000_000 / 0.8 * 2))

def perform_async(num_feature_batches: int, fraction_of_io: float):
    async def tasks():
        await asyncio.gather(*[prepare_feature_batch(preprocessing=True, fraction_of_io=fraction_of_io) for _ in range(num_feature_batches)])

    asyncio.run(
        tasks()
    )

def perform_threaded(num_feature_batches: int, fraction_of_io: float):
    with ThreadPoolExecutor(max_workers=num_feature_batches) as executor:
        futures = [executor.submit(prepare_feature_batch_serial, preprocessing=True, fraction_of_io=fraction_of_io) for _ in range(num_feature_batches)]
        results = [future.result() for future in as_completed(futures)]
    
    return results

def perform_multiprocessing(num_feature_batches: int, fraction_of_io: float):
    with ProcessPoolExecutor(max_workers=num_feature_batches) as executor:
        futures = [executor.submit(prepare_feature_batch_serial, preprocessing=True, fraction_of_io=fraction_of_io) for _ in range(num_feature_batches)]
        results = [future.result() for future in as_completed(futures)]
    
    return results
def perform_serial(num_feature_batches: int, fraction_of_io: float):
    for _ in range(num_feature_batches):
        prepare_feature_batch_serial(preprocessing=True, fraction_of_io=fraction_of_io)

if __name__ == "__main__":
    results = []
    TASKS = [1, 2, 4, 8, 16, 32]

    experiments = [("multiprocessing", 0.5)]

    for experiment_type, fraction_of_io in experiments:
    # for experiment_type in ["serial", "async"]:
        # 1.0 - 50% CPU, 50% I/O
        # for fraction_of_io in [0.0, 0.5, 1.0]:
            results.append({
                "name": f"python_{experiment_type}_cpu_fraction_{fraction_of_io}",
                "times": [],
                "tasks": TASKS
            })

            for num_feature_batches in TASKS:
                    
                    start_time = time.time()

                    if experiment_type == "serial":
                        perform_serial(num_feature_batches, fraction_of_io)
                    else:
                        if os.environ.get("PYTHON_GIL") == "0":
                            print("Overrided by PYTHON_GIL=0, running with nogil and threading.")
                            perform_threaded(num_feature_batches, fraction_of_io)
                        else:
                            if experiment_type == "async":
                                import asyncio
                                import aiohttp
                                perform_async(num_feature_batches, fraction_of_io)
                            else:
                                perform_multiprocessing(num_feature_batches, fraction_of_io)
                        
                    end_time = time.time()

                    results[-1]["times"].append(end_time - start_time)

                    print(f"{experiment_type}_{num_feature_batches} tasks, CPU fraction of I/O: {fraction_of_io}, time taken: ", end_time - start_time)

    print(json.dumps(results, indent=4))