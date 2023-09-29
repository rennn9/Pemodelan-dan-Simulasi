"""
Python version: 3.7.3
SimPy version: 3.0.11
"""

import simpy
import random
import numpy as np

class Drive_thru(object):
    def __init__(self, env):
        self.env = env
        self.food_server = simpy.Resource(env, 1)
        self.order = simpy.Resource(env, 1)

    def place_order(self, customer, values, env):
        waktu_pelayanan = random.choice(values)
        print(f'Customer#{customer+1} is ordering.....time:{env.now}')
        yield self.env.timeout(waktu_pelayanan)

    def take_food(self, customer, env, values):
        waktu_pelayanan = random.choice(values)
        print(f'Customer#{customer+1} is taking food.....time:{env.now}')
        yield self.env.timeout(waktu_pelayanan)

    def walking_to_food_server(self, customer, env, values):
        waktu_jalan = random.choice(values)
        print(f'Customer#{customer+1} is walking to food server.....time:{env.now}')
        yield self.env.timeout(waktu_jalan)
    
    def leaving(self, customer, env):
        print(f'Customer#{customer+1} is leaving.....time:{env.now}')
        yield self.env.timeout(0)


def arrive_at_drive_thru(env, customer, drive_thru, values_2, values_3, values_4, record):
    # customer arrives at the drive_thru
    print(f'Customer#{customer+1} is arriving.....time:{env.now}')
    record[customer].append(env.now)

    with drive_thru.order.request() as request:
        yield request
        yield env.process(drive_thru.place_order(customer, values_2, env))
    with drive_thru.order.request() as request:
        yield request
        yield env.process(drive_thru.walking_to_food_server(customer, env, values_4))
    if random.choice([True, False]):
        with drive_thru.food_server.request() as request:
            yield request
            yield env.process(drive_thru.take_food(customer, env, values_3))
            yield env.process(drive_thru.leaving(customer, env))
    record[customer].append(env.now)


def drive_thru(env, values, values_2, values_3, values_4, record):
    drive_thru = Drive_thru(env)

    for customer in range(3):
        record.append([])
        env.process(arrive_at_drive_thru(env, customer, drive_thru, values_2, values_3, values_4, record))

    while True:
        yield env.timeout(random.choice(values))  # Wait a bit before generating a new person

        customer += 1
        record.append([])
        env.process(arrive_at_drive_thru(env, customer, drive_thru, values_2, values_3, values_4, record))
    

def main():
    # Setup
    random.seed(42)
    data_record = []
    Mean_selang_kedatangan = 3.03
    Standard_deviation_selang_kedatangan = 1.66
    size = 30
    Mean_server_1 = 1.9
    Standard_deviation_server_1 = 1
    Mean_server_2 = 2.1
    Standard_deviation_server_2 = 1.76
    Mean_walking = 0.47
    Standard_deviation_walking = 0.65

    server_1=list(filter(lambda x : x >= 0, np.random.normal(Mean_server_1, Standard_deviation_server_1, size))) 

    values=list(filter(lambda x : x >= 0, np.random.normal(Mean_selang_kedatangan, Standard_deviation_selang_kedatangan, size))) 

    server_2=list(filter(lambda x : x >= 0, np.random.normal(Mean_server_2, Standard_deviation_server_2, size)))

    walking=list(filter(lambda x : x >= 0, np.random.normal(Mean_walking, Standard_deviation_walking, size)))

    
    # Run the simulation
    env = simpy.Environment()
    
    print(values)
    print(  "Running simulation..." )
    
    env.process(drive_thru(env, values, server_1, server_2, walking, data_record))
    env.run(until=90)
    # print(data_record)

    data_record_filter = list(filter(lambda x : len(x)==2, data_record)) 

    sum = 0
    for drive_thru_customer in data_record_filter:
        sum += drive_thru_customer[1]-drive_thru_customer[0]
    
    average = sum/len(data_record_filter)
    print(f'Rata-rata waktu tunggu: {average}')

if __name__ == "__main__":
    main()