import sys
from cache import *
import numpy as np
import random

if __name__ == "__main__":
	filepath = sys.argv[1]

	disk_read_speed = 10
	disk_write_speed = 10
	cache_size=5
	cache_read_speed = 1
	cache_write_speed = 1
	cache_writethrough = True

	memory = Disk(disk_read_speed,disk_write_speed)
	ram = LIRS(cache_size,cache_read_speed,cache_write_speed,memory,cache_writethrough)

	random.seed(42)

	with open(filepath, "r") as trace_file:
		successes = []
		read_times = []
		write_times = []

		i = 0
		for line in trace_file.readlines():
			if i == 1000:
				break
			timestamp, obj_id, obj_size = line.split(",")

			is_read = random.choices([True, False], weights = [90, 10])[0]

			if is_read:
				success, time = ram.read(obj_id)
				read_times.append(time)
			else:
				success, time = ram.write(obj_id)
				write_times.append(time)

			successes.append(success)
			i+=1

	count = len(successes)

	successes = np.array(successes)
	print("Num Requests: ", count)
	print("Num Reads: ", len(read_times))
	print("Num Writes: ", len(write_times))
	print("Success rate: ", len(successes[successes]) / float(count))
	print("Average read time: ", np.average(read_times))
	print("Average write time: ", np.average(read_times))