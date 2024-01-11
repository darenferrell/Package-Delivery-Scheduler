
class Packages:
    def __init__(self, identification, address, city, state, zipcode, package_delivery_deadline_time, weight, status):
        self.identification = identification
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.package_delivery_deadline_time = package_delivery_deadline_time
        self.weight = weight
        self.status = status
        self.actual_departure_time = None
        self.actual_delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.identification, self.address, self.city, self.state,
                                                       self.zipcode, self.package_delivery_deadline_time, self.weight,
                                                       self.actual_delivery_time, self.status)

    def update_delivery_status(self, convert_timedelta):
        if self.actual_delivery_time < convert_timedelta:
            self.status = "Package has been delivered"
        elif self.actual_departure_time > convert_timedelta:
            self.status = "On the way"
        else:
            self.status = "Arrived at hub"
