import sys
from cache import *
import numpy as np
import random

if __name__ == "__main__":
	filepath = sys.argv[1]

	disk_read_speed = 10
	disk_write_speed = 10
	cache_size = 50000
	cache_read_speed = 1
	cache_write_speed = 1
	cache_writethrough = True
	adds_reads_to_cache = True

	percent_reads = 50
	percent_writes = 100 - percent_reads

	memory = Disk(disk_read_speed, disk_write_speed)
	ram = LIRS(cache_size, cache_read_speed, cache_write_speed, memory, cache_writethrough, adds_reads_to_cache)

	random.seed(42)

	with open(filepath, "r") as trace_file:
		successes = []
		read_times = []
		write_times = []

		read_hits = 0
		read_misses = 0
		write_hits = 0
		write_misses = 0

		lines = trace_file.readlines()

		i = 0
		for line in lines:
			if i == 50000:
				break

			timestamp, obj_id, obj_size = line.split(",")

			is_read = random.choices([True, False], weights = [percent_reads, percent_writes])[0]

			if is_read:
				success, is_hit, time = ram.read(obj_id)
				read_times.append(time)

				if is_hit: read_hits += 1
				else: read_misses +=1
			else:
				success, is_hit, time = ram.write(obj_id, int(obj_size))
				write_times.append(time)

				if is_hit: write_hits += 1
				else: write_misses +=1

			successes.append(success)
			i+=1

	count = len(successes)
	successes = np.array(successes)
	hits = read_hits + write_hits
	misses = read_misses + write_misses

	print("Num Requests: ", count)
	print("%% Reads: %0.2f%%" % (100 * len(read_times) / count))
	print("%% Writes: %0.2f%%" % (100 * len(write_times) / count))
	print("%% Read Hits: %0.2f%%" % (100 * read_hits / (read_hits + read_misses)))
	print("%% Read Misses: %0.2f%%" % (100 * read_misses / (read_hits + read_misses)))
	print("%% Write Hits: %0.2f%%" % (100 * write_hits / (write_hits + write_misses)))
	print("%% Write Misses: %0.2f%%" % (100 * write_misses / (write_hits + write_misses)))
	print("%% Hits: %0.2f%%" % (100 * hits / (hits + misses)))
	print("%% Misses: %0.2f%%" % (100 * misses / (hits + misses)))
	print("Success rate: %0.2f%%" % (100 * len(successes[successes]) / count))
	print("Read times – Mean: %0.2f, Stdev: %0.2f" % (np.average(read_times), np.std(read_times)))
	print("Write times – Mean: %0.2f, Stdev: %0.2f" % (np.average(write_times), np.std(write_times)))