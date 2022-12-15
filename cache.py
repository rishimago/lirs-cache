from sys import maxsize as infinity

class Disk:
    def __init__ (self,read_speed,write_speed):
        self.read_speed = read_speed
        self.write_speed = write_speed
        self.mem = {}
    def read(self,key):
      if(key in self.mem.keys()):
        return True, self.mem[key], self.read_speed
      else:
          return False, None, self.read_speed
    def write(self,key,size):
      self.mem[key] = size
      return True, self.write_speed


class LIRS:
    def __init__(self,size,read_speed,write_speed,fallback,writethrough,add_reads_to_cache):
        self.maxBytes = size
        self.read_speed = read_speed
        self.write_speed = write_speed
        self.fallback = fallback
        self.mem = {}
        self.bytesStored = 0
        self.recency_times = {}
        self.last_access = {}
        self.writethrough = writethrough
        self.num_accesses = 0
        self.add_reads_to_cache = add_reads_to_cache

    def read(self,key):
        self.num_accesses += 1
        if(key in self.last_access.keys()):
          self.recency_times[key] = self.num_accesses - self.last_access[key]
        self.last_access[key] = self.num_accesses
        if(key in self.mem.keys()):
            return True, True, self.read_speed
        else:
            succ, size, time = self.fallback.read(key)

            if succ and self.add_reads_to_cache:
              while (self.bytesStored + size >= self.maxBytes):
                if self.bytesStored == 0:
                  return True, False, (time + self.read_speed)

                #find worst key
                best_item = None
                best_lir = infinity
                best_tiebreaker = infinity

                for item, item_size in self.mem.items():
                  last = self.last_access[item]
                  recency = self.recency_times[item]
                  lir = max(recency, self.num_accesses - last)
                  tiebreaker = min(recency, self.num_accesses - last)
                  if(lir < best_lir):
                    best_lir = lir
                    best_tiebreaker = tiebreaker
                    best_item = item 
                    best_size = item_size
                  elif((lir == best_lir) and (tiebreaker < best_tiebreaker)):
                    best_tiebreaker = tiebreaker 
                    best_item = item 
                    best_size = item_size

                self.mem.pop(best_item)
                self.bytesStored -= best_size
                if(not self.writethrough):
                  success,accrued_time = self.fallback.write(best_item, best_size)
                  time += accrued_time

              self.mem[key] = size
              self.bytesStored += size

            return succ, False, (time + self.read_speed)
    def write(self,key,size):
        self.num_accesses += 1
        if(key in self.last_access.keys()):
          self.recency_times[key] = self.num_accesses - self.last_access[key]
        else:
          self.recency_times[key] = infinity
        self.last_access[key] = self.num_accesses
        if(self.writethrough):
          success, accrued_time = self.fallback.write(key, size)
        else:
          accrued_time = 0
        
        if(key in self.mem.keys()):
            return True, True, self.write_speed + accrued_time
        else:
          while (self.bytesStored + size >= self.maxBytes):
            if self.bytesStored == 0:
              return False, False, self.write_speed + accrued_time

            #find worst key
            best_item = None
            best_lir = infinity
            best_tiebreaker = infinity

            for item, item_size in self.mem.items():
              last = self.last_access[item]
              recency = self.recency_times[item]
              lir = max(recency, self.num_accesses - last)
              tiebreaker = min(recency, self.num_accesses - last)
              if(lir < best_lir):
                best_lir = lir
                best_tiebreaker = tiebreaker
                best_item = item 
                best_size = item_size
              elif((lir == best_lir) and (tiebreaker < best_tiebreaker)):
                best_tiebreaker = tiebreaker 
                best_item = item 
                best_size = item_size

            self.mem.pop(best_item)
            self.bytesStored -= best_size
            if(not self.writethrough):
              success,time = self.fallback.write(best_item, best_size)
              accrued_time += time

          self.mem[key] = size
          self.bytesStored += size
          return True, False, self.write_speed + accrued_time
          
memory = Disk(10,10)
ram = LIRS(5,1,1,memory,True,True)

if __name__ == "__main__":
  for i in range(100):
      a,b,c = ram.write(i, 1)

  for i in range(100):
      for j in range(10):
          print(ram.read(i))