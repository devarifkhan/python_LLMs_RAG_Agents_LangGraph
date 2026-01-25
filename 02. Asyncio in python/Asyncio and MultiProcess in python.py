
import asyncio
import aiohttp
import time
from multiprocessing import Pool, cpu_count

def process_content(args):
	url, content = args
	print(f"Processing content from {url} (size: {len(content)} bytes) in process")
	# Simulate CPU-bound processing
	time.sleep(1)
	print(f"Finished processing {url}")

async def download_page(session, url):
	print(f"Starting download: {url}")
	async with session.get(url) as response:
		content = await response.read()
	print(f"Downloaded: {url}")
	return (url, content)

async def main():
	urls = [
		"https://www.example.com",
		"https://www.python.org",
		"https://www.wikipedia.org",
		"https://www.github.com"
	]
	async with aiohttp.ClientSession() as session:
		tasks = [download_page(session, url) for url in urls]
		results = await asyncio.gather(*tasks)

	with Pool(processes=cpu_count()) as pool:
		pool.map(process_content, results)

if __name__ == "__main__":
	start = time.time()
	asyncio.run(main())
	end = time.time()
	print(f"Total time taken: {end - start:.2f} seconds")
