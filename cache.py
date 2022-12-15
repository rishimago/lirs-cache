from bisect import insort

class Disk:
    def __init__ (self,read_speed,write_speed):
        self.read_speed = read_speed
        self.write_speed = write_speed
        self.mem = set()
    def read(self,key):
      if(key in self.mem):
        return True,self.read_speed
      else:
          return False,0
    def write(self,key):
      self.mem.add(key)
      return True,self.write_speed


class LIRS:
    def __init__(self,size,read_speed,write_speed,fallback,writethrough):
        self.size = size
        self.read_speed = read_speed
        self.write_speed = write_speed
        self.fallback = fallback
        self.mem = PriorityQueue(self.size)
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
        self.last_access[key] = self.num_accesses
        if(self.writethrough):
          success, accrued_time = fallback.write(key)
        else:
          accrued_time = 0
        
        if(key in self.mem):
            return True, self.write_speed + accrued_time
