import sys
from cache import *
import numpy as np
import random

if __name__ == "__main__":
	filepath = sys.argv[1]

	disk_read_speed = 10
	disk_write_speed = 10
	cache_size = 5
	cache_read_speed = 1
	cache_write_speed = 1
	cache_writethrough = False

	percent_reads = 50
	percent_writes = 100 - percent_reads

	memory = Disk(disk_read_speed,disk_write_speed)
	ram = LIRS(cache_size,cache_read_speed,cache_write_speed,memory,cache_writethrough)

	random.seed(42)

	with open(filepath, "r") as trace_file:
		successes = []
		read_times = []
		write_times = []

		hits = 0
		misses = 0

		lines = trace_file.readlines()

		i = 0
		for line in lines:
			if i == 50000:
				break

			timestamp, obj_id, obj_size = line.split(",")

			is_read = random.choices([True, False], weights = [percent_reads, percent_writes])[0]

			if is_read:
				success, time = ram.read(obj_id)
				read_times.append(time)

				# if time == disk_read_speed + cache_read_speed:
				# 	hits += 1
			else:
				success, time = ram.write(obj_id)
				write_times.append(time)

			successes.append(success)
			i+=1

		i = 0
		for line in lines:
			if i == 50000:
				break

			timestamp, obj_id, obj_size = line.split(",")

			is_read = random.choices([True, False], weights = [percent_reads, percent_writes])[0]

			if is_read:
				success, time = ram.read(obj_id)
				read_times.append(time)

				# if time == disk_read_speed + cache_read_speed:
				# 	hits += 1
			else:
				success, time = ram.write(obj_id)
				write_times.append(time)

			successes.append(success)
			i+=1

	count = len(successes)

	successes = np.array(successes)
	print("Num Requests: ", count)
	print("% Reads: ", len(read_times) / float(count))
	print("% Writes: ", len(write_times) / float(count))
	print("Success rate: ", len(successes[successes]) / float(count))
	print("Read times – Mean: ", np.average(read_times), "Stdev: ", np.std(read_times))
	print("Write times – Mean: ", np.average(write_times), "Stdev: ", np.std(write_times))