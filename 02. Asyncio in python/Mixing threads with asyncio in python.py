
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time

def process_content(url, content):
	print(f"Processing content from {url} (size: {len(content)} bytes) in thread")
	# Simulate CPU-bound processing
	time.sleep(1)
	print(f"Finished processing {url}")

async def download_and_process(url, session, executor):
	print(f"Starting download: {url}")
	async with session.get(url) as response:
		content = await response.read()
	print(f"Downloaded: {url}, submitting to thread pool")
	loop = asyncio.get_running_loop()
	await loop.run_in_executor(executor, process_content, url, content)

async def main():
	urls = [
		"https://www.example.com",
		"https://www.python.org",
		"https://www.wikipedia.org",
		"https://www.github.com"
	]
	executor = ThreadPoolExecutor(max_workers=4)
	async with aiohttp.ClientSession() as session:
		tasks = [download_and_process(url, session, executor) for url in urls]
		await asyncio.gather(*tasks)
	executor.shutdown()

if __name__ == "__main__":
	start = time.time()
	asyncio.run(main())
	end = time.time()
	print(f"Total time taken: {end - start:.2f} seconds")
