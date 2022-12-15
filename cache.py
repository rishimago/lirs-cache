class Disk:
    
    def __init__ (self,read_speed,write_speed):
        self.read_speed = read_speed
        self.write_speed = write_speed

class LIRS:
    def __init__(self,size,read_speed,write_speed,fallback,writethrough):
        self.size = size
        self.read_speed = read_speed
        self.write_speed = write_speed
        self.fallback = fallback