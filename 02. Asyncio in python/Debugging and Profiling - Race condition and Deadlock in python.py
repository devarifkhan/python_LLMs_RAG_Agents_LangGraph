
# Example 1: Race Condition (Bank Account)
import threading
import time

class BankAccount:
	def __init__(self):
		self.balance = 0

	def deposit(self, amount):
		temp = self.balance
		time.sleep(0.01)  # Simulate processing delay
		self.balance = temp + amount

def make_deposits(account, n):
	for _ in range(n):
		account.deposit(1)

def race_condition_demo():
	account = BankAccount()
	threads = [threading.Thread(target=make_deposits, args=(account, 100)) for _ in range(5)]
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	print(f"Final balance (should be 500): {account.balance}")

print("--- Race Condition Demo ---")
race_condition_demo()

# Example 2: Deadlock (Resource Locking)
def deadlock_demo():
	lock_a = threading.Lock()
	lock_b = threading.Lock()

	def thread1():
		with lock_a:
			print("Thread 1 acquired lock_a")
			time.sleep(0.1)
			with lock_b:
				print("Thread 1 acquired lock_b")

	def thread2():
		with lock_b:
			print("Thread 2 acquired lock_b")
			time.sleep(0.1)
			with lock_a:
				print("Thread 2 acquired lock_a")

	t1 = threading.Thread(target=thread1)
	t2 = threading.Thread(target=thread2)
	t1.start()
	t2.start()
	t1.join(timeout=1)
	t2.join(timeout=1)
	print("If you see this message and both threads are stuck, a deadlock occurred!")

print("\n--- Deadlock Demo ---")
deadlock_demo()
