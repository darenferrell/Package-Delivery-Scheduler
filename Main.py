# Author: Daren Ferrell
# Student ID: 000777520
# WGU PS Package Delivery Program

import csv
import datetime
import Trucks
from builtins import ValueError

from CreateHashTable import CreateHashMap
from Packages import Packages

# This is the method for reading the distances file
with open("CSV/Distances_File.csv") as csvfile:
    CSV_Dist = csv.reader(csvfile)
    CSV_Dist = list(CSV_Dist)

# This is the method for reading the packages file
with open("CSV/Packages_File.csv") as csvfile1:
    CSV_Pack = csv.reader(csvfile1)
    CSV_Pack = list(CSV_Pack)

# This is the method for reading the addresses file
with open("CSV/Addresses_File.csv") as csvfile2:
    CSV_Addr = csv.reader(csvfile2)
    CSV_Addr = list(CSV_Addr)


# This is the method that creates package objects from Packages_File.csv and then loads said objects into the hash table
def load_data_for_package(filename, hash_table_for_pack):
    with open(filename) as pack_information:
        data_for_package = csv.reader(pack_information)
        for pack in data_for_package:
            pack_id = int(pack[0])
            package_address = pack[1]
            package_city = pack[2]
            package_state = pack[3]
            package_zipcode = pack[4]
            package_delivery_deadline_time = pack[5]
            package_weight = pack[6]
            package_status = "Arrived at hub"
            pack = Packages(pack_id, package_address, package_city, package_state, package_zipcode,
                            package_delivery_deadline_time, package_weight, package_status)

            hash_table_for_pack.insert(pack_id, pack)


# This is the method that calculates the distance between two given addresses
def distance_between_packages(x, y):
    dist = CSV_Dist[x][y]
    if dist == '':
        dist = CSV_Dist[y][x]
    return float(dist)


# This is the method that extracts the address number from the string literal of the address value
def addr_extr(selected_address):
    for row in CSV_Addr:
        if selected_address in row[2]:
            return int(row[0])
    print("bad address: ", selected_address)


# This method creates an object for Truck #1
truck1 = Trucks.Trucks(16, 18, None, [7, 2, 4, 5, 8, 10, 11, 12, 17, 20, 21, 22, 23, 24, 26, 27],
                       0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# This method creates an object for Truck #2
truck2 = Trucks.Trucks(16, 18, None, [3, 6, 18, 25, 28, 32, 36, 38], 0.0,
                       "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# This method creates an object for Truck #3
truck3 = Trucks.Trucks(16, 18, None, [1, 13, 9, 14, 15, 16, 19, 29, 30, 31, 34, 37, 40, 33, 35, 39],
                       0.0, "4001 South 700 East", datetime.timedelta(hours=8))

hash_table_for_pack = CreateHashMap()

# This method loads packages into the hash table
load_data_for_package("CSV/Packages_File.csv", hash_table_for_pack)


# This is the method that utilizes the Nearest Neighbor Algorithm to determine which packages should be ordered next and
# also determines how far a truck has driven after delivering a particular package
def package_delivery_process(selected_truck):
    # Puts all of the packages into an array entitled 'undelivered'
    undelivered = []
    for pack_id in selected_truck.packages:
        pack = hash_table_for_pack.lookup(pack_id)
        undelivered.append(pack)
    # Pulls package information from the hash table
    selected_truck.packages.clear()
    # clears out the packages list so that packages can be placed in order determined by the Nearest Neighbor algorithm
    while len(undelivered) > 0:
        upcoming_address = 2000
        upcoming_package = None
        # loops through entire list of undelivered packages
        for pack in undelivered:
            if distance_between_packages(addr_extr(selected_truck.address),
                                         addr_extr(pack.address)) <= upcoming_address:
                upcoming_address = distance_between_packages(addr_extr(selected_truck.address),
                                                             addr_extr(pack.address))
                upcoming_package = pack
        # calculates next closest package for delivery and adds said package to list
        selected_truck.packages.append(upcoming_package.identification)

        undelivered.remove(upcoming_package)
        # removes package that has just been delivered from the 'undelivered' list
        selected_truck.miles += upcoming_address
        # calculates mileage of delivery and adds it to mileage total
        selected_truck.address = upcoming_package.address
        # updates truck address so that algorithm can begin next calculation based on truck locatio
        selected_truck.time += datetime.timedelta(hours=upcoming_address / 18)
        # updates time that was required for truck to travel to nearest address
        upcoming_package.actual_delivery_time = selected_truck.time

        upcoming_package.actual_departure_time = selected_truck.dep_time


package_delivery_process(truck1)
# commences loading process for truck 1
package_delivery_process(truck2)
# commences loading process for truck 2
truck3.dep_time = min(truck1.time, truck2.time)
# ensures that truck 3 does not load until the first two trucks have completed their deliveries
package_delivery_process(truck3)

# This method creates an interface for the user and displays information
print("Western Governors University Parcel Service (WGU PS)")
print("The total route mileage adds up to:")
print(truck1.miles + truck2.miles + truck3.miles)

input_text = input("To initialize package status check, please type 'status' (Any other text entry will cause the "
                   "program to close.)")

if input_text == "status":
    try:
        user_status = input(
            "In order to check the status of a particular package or packages, please enter the time of "
            "day in the format of hh:mm:ss")

        (h, m, s) = user_status.split(":")
        convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        quantity_input = input(
            "In order to view the status of one package, type '1'. Otherwise, in order to view the "
            "status of all packages, type '2'")

        if quantity_input == "1":
            try:
                identification_input = input("Please enter the package identification number.")
                p = hash_table_for_pack.lookup(int(identification_input))
                p.update_delivery_status(convert_timedelta)
                print(str(p))
            except ValueError:
                print("That is not a valid entry. Program will now close.")
                exit()

        elif quantity_input == "2":
            try:

                for identification in range(1, 41):
                    pack = hash_table_for_pack.lookup(identification)
                    pack.update_delivery_status(convert_timedelta)
                    print(str(pack))

            except ValueError:
                print("That is not a valid entry. Program will now close.")
                exit()
        else:
            exit()

    except ValueError:
        print("That is not a valid entry. Program will now close.")
        exit()

elif input != "status":
    print("That is not a valid entry. Program will now close.")
    exit()
