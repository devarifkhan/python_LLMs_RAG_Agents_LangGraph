import threading
import time
import requests

def download_page(url):
    print(f"Starting download: {url}")
    response = requests.get(url)
    print(f"Finished download: {url} (size: {len(response.content)} bytes)")

urls = [
    "https://www.example.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.github.com"
]

start = time.time()

threads = []
for url in urls:
    t = threading.Thread(target=download_page, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()
print(f"Total time taken: {end - start:.2f} seconds")