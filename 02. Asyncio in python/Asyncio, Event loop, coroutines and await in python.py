
import asyncio
import aiohttp
import time

async def download_page(session, url):
	print(f"Starting download: {url}")
	async with session.get(url) as response:
		content = await response.read()
		print(f"Finished download: {url} (size: {len(content)} bytes)")

async def main():
	urls = [
		"https://www.example.com",
		"https://www.python.org",
		"https://www.wikipedia.org",
		"https://www.github.com"
	]
	async with aiohttp.ClientSession() as session:
		tasks = [download_page(session, url) for url in urls]
		await asyncio.gather(*tasks)

if __name__ == "__main__":
	start = time.time()
	asyncio.run(main())
	end = time.time()
	print(f"Total time taken: {end - start:.2f} seconds")
