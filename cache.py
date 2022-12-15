from sys import maxsize as infinity

class Disk:
    def __init__ (self,read_speed,write_speed):
        self.read_speed = read_speed
        self.write_speed = write_speed
        self.mem = set()
    def read(self,key):
      if(key in self.mem):
        return True,self.read_speed
      else:
          return False,self.read_speed
    def write(self,key):
      self.mem.add(key)
      return True,self.write_speed


class LIRS:
    def __init__(self,size,read_speed,write_speed,fallback,writethrough):
        self.size = size
        self.read_speed = read_speed
        self.write_speed = write_speed
        self.fallback = fallback
        self.mem = set()
        self.recency_times = {}
        self.last_access = {}
        self.writethrough = writethrough
        self.num_accesses = 0
    def read(self,key):
        self.num_accesses += 1
        if(key in self.last_access.keys()):
          self.recency_times[key] = self.num_accesses - self.last_access[key]
        self.last_access[key] = self.num_accesses
        if(key in self.mem):
            return True, self.read_speed
        else:
            succ, time = self.fallback.read(key)
            return succ,(time + self.read_speed)
    def write(self,key):
        self.num_accesses += 1
        if(key in self.last_access.keys()):
          self.recency_times[key] = self.num_accesses - self.last_access[key]
        else:
          self.recency_times[key] = infinity
        self.last_access[key] = self.num_accesses
        if(self.writethrough):
          success, accrued_time = self.fallback.write(key)
        else:
          accrued_time = 0
        
        if(key in self.mem):
            return True, self.write_speed + accrued_time
        elif(len(self.mem) < self.size):
            self.mem.add(key)
            return True, self.write_speed + accrued_time
        else:
          #find worst key
          best_item = None
          best_lir = infinity
          best_tiebreaker = infinity
          for item in self.mem:
            last = self.last_access[item]
            recency = self.recency_times[item]
            lir = max(recency, self.num_accesses - last)
            tiebreaker = min(recency, self.num_accesses - last)
            if(lir < best_lir):
              best_lir = lir
              best_tiebreaker = tiebreaker
              best_item = item 
            elif((lir == best_lir) and (tiebreaker < best_tiebreaker)):
              best_tiebreaker = tiebreaker 
              best_item = item 
          self.mem.remove(best_item)
          if(not self.writethrough):
            success,accrued_time = self.fallback.write(best_item)
          self.mem.add(key)
          return True, self.write_speed + accrued_time
          
memory = Disk(10,10)
ram = LIRS(5,1,1,memory, True)

if __name__ == "__main__":
  for i in range(100):
      a,b = ram.write(i)

  for i in range(100):
      for j in range(10):
          print(ram.read(i))