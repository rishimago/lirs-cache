import sys
from cache import *
import numpy as np
import random
import matplotlib.pyplot as plt

def run_trial(ram, state):
  random.setstate(state)

  with open(filepath, "r") as trace_file:
    successes = []
    read_times = []
    write_times = []

    read_hits = 0
    read_misses = 0
    write_hits = 0
    write_misses = 0

    lines = trace_file.readlines()[:100000]

    ids = {}
    sizes = []

    for line in lines:
      timestamp, obj_id, obj_size = line.split(",")
      obj_size = int(obj_size)

      if obj_id in ids.keys():
        ids[obj_id] += 1
      else:
        ids[obj_id] = 1
        sizes.append(obj_size)

      is_read = random.choices([True, False], weights = [percent_reads, percent_writes])[0]

      if is_read:
        success, is_hit, time = ram.read(obj_id)
        read_times.append(time)

        if is_hit: read_hits += 1
        else: read_misses +=1
      else:
        success, is_hit, time = ram.write(obj_id, obj_size)
        write_times.append(time)

        if is_hit: write_hits += 1
        else: write_misses +=1

      successes.append(success)

  count = len(successes)
  successes = np.array(successes)
  hits = read_hits + write_hits
  misses = read_misses + write_misses
  times = np.append(read_times, write_times)

  num_items = len(ids.keys())
  sizes = np.array(sizes)

  print("Num Requests: ", count)
  print("Distinct items: ", num_items)
  print("Object size stats – Mean: %0.2f, Stdev: %0.2f, Min: %0.2f, Max: %0.2f" % (np.mean(sizes), np.std(sizes), np.min(sizes), np.max(sizes)))
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
  print("Overall times – Mean: %0.2f, Stdev: %0.2f" % (np.average(times), np.std(times)))

  values = np.array(list(ids.values()))
  
  return values


if __name__ == "__main__":
  filepath = sys.argv[1]

  disk_read_speed = 10
  disk_write_speed = 10
  cache_size = int(sys.argv[2])
  cache_read_speed = 1
  cache_write_speed = 1
  cache_writethrough = True
  adds_reads_to_cache = True

  percent_reads = 50
  percent_writes = 100 - percent_reads

  memory = Disk(disk_read_speed, disk_write_speed)
  lirs_ram = LIRS(cache_size, cache_read_speed, cache_write_speed, memory, cache_writethrough, adds_reads_to_cache)
  fifo_ram = FIFO(cache_size, cache_read_speed, cache_write_speed, memory, cache_writethrough, adds_reads_to_cache)
  lru_ram = LRU(cache_size, cache_read_speed, cache_write_speed, memory, cache_writethrough, adds_reads_to_cache)

  random.seed(42)
  rand = random.getstate()

  print("LIRS:")
  run_trial(lirs_ram, rand)
  print("\nFIFO:")
  run_trial(fifo_ram, rand)
  print("\nLRU:")
  values = run_trial(lru_ram, rand)
  # print(values)
  # print(np.mean(values))
  # print(np.std(values))
  # print(np.min(values))
  # print(np.max(values))
  plt.hist(values, bins = 200)
  plt.show()
  print("\nDone!")