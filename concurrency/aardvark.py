import asyncio
from concurrent.futures import ProcessPoolExecutor
import functools
import time

#from tqdm import tqdm
#from tqdm.asyncio import tqdm_asyncio

from aiofiles import open

async def read_file(filename: str):
    """ We will use the aiofiles API to read the files concurrently """
    async with open(filename, "r", encoding="utf-8") as f:
        return await f.readlines()

async def get_all_file_content(file_names: list[str]):
    """ Start concurrent tasks and join the file contents together """
    print("Begin to read files...")
    start = time.monotonic()
    tasks, results = [], []

    for filename in file_names:
        tasks.append(asyncio.create_task(read_file(filename)))
    temp_results = await asyncio.gather(*tasks)

    results = [item for sublist in temp_results for item in sublist]
    print(f"All files are read in {time.monotonic() - start:.2f} second(s)")
    return results

def partition(contents: list[str], partition_size: int):
    """ Split the contents into multiple lists of partition_size length and return them as generator """
    for i in range(0, len(contents), partition_size):
        yield contents[i: i+partition_size]

def map_resource(chunk: list[str]) -> dict[str, int]:
    """ The method that actually performs the map task
    returns the sum of the counts corresponding to the keywords in the current partition.
    """
    result = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if word in result:
            result[word] = result[word] + int(count)
        else:
            result[word] = int(count)

    return result

async def map_with_process(chunks: list[list[str]]):
    """ Execute map tasks in parallel and join the results of multiple processes into lists """
    print("Start parallel execution of map tasks...")
    start = time.monotonic()
    loop = asyncio.get_running_loop()
    tasks = []

    with ProcessPoolExecutor() as executor:
        for chunk in chunks:
            tasks.append(loop.run_in_executor(executor, map_resource, chunk))

    print(f"All map tasks are executed in {time.monotonic()-start:.2f} second(s)")
    return await asyncio.gather(*tasks)

def merge_resource(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    """ The actually reduce method sums the counts of two dicts with the same key """
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged

def reduce(intermediate_results: list[dict[str, int]]) -> dict[str, int]:
    """ Use the functools.reduce method to combine all the items in the list """
    return functools.reduce(merge_resource, intermediate_results)

async def main(partition_size: int):
    """ Entrance to all methods """
    file_names = ["data/googlebooks-eng-all-1gram-20120701-a",
                  "data/googlebooks-eng-all-1gram-20120701-b",
                  "data/googlebooks-eng-all-1gram-20120701-c"]
    contents = await get_all_file_content(file_names)
    chunks = partition(contents, partition_size)
    intermediate_results = await map_with_process(chunks)
    final_results = reduce(intermediate_results)

    print(f'Aardvark has appeared {final_results["Aardvark"]} times.')

if __name__ == "__main__":
    asyncio.run(main(partition_size=60_000))
