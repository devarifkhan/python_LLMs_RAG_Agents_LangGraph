from multiprocessing import Process
import time
import random

def process_image(image_id):
    print(f"Processing image {image_id}...")
    # Simulate CPU-bound work
    time.sleep(random.uniform(1, 2))
    print(f"Finished processing image {image_id}")

if __name__ == "__main__":
    image_ids = ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"]
    start_time = time.time()

    processes = []
    for img in image_ids:
        p = Process(target=process_image, args=(img,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")