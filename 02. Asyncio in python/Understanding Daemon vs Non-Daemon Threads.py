
import threading
import time
import os

def write_to_file():
	with open("daemon_example.txt", "w") as f:
		for i in range(5):
			f.write(f"Writing line {i+1}\n")
			print(f"Daemon thread: wrote line {i+1}")
			time.sleep(1)
	print("Daemon thread: finished writing")

def cleanup_task():
	print("Non-daemon thread: starting cleanup")
	time.sleep(3)
	if os.path.exists("daemon_example.txt"):
		os.remove("daemon_example.txt")
		print("Non-daemon thread: file cleaned up!")
	else:
		print("Non-daemon thread: file not found!")

if __name__ == "__main__":
	daemon_thread = threading.Thread(target=write_to_file, daemon=True)
	non_daemon_thread = threading.Thread(target=cleanup_task, daemon=False)

	daemon_thread.start()
	non_daemon_thread.start()

	print("Main thread: sleeping for 2 seconds...")
	time.sleep(2)
	print("Main thread: exiting now!")

	# Only join the non-daemon thread to show the difference
	non_daemon_thread.join()
	print("Main thread: program finished.")
