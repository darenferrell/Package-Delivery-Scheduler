class Trucks:
    def __init__(self, capacity, speed, load, packages, miles, address, dep_time):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.miles = miles
        self.address = address
        self.dep_time = dep_time
        self.time = dep_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load,
                                               self.packages, self.miles, self.address,
                                               self.dep_time)