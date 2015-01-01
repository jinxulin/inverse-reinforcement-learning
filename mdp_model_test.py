from driving.model import *
"""
car_groups = []
for i in range(100):
    car = Car(1, 20, 40, 50)
    car_groups.append(car)
    print len(car_groups)

car_groups = [car for car in car_groups if car.pos < 540 or car.pos > 0]
print len(car_groups)
"""

model = DrivingModel()
for i in range(200):
    action = random.randint(0, 4)
    print action
    print model.trans(None, action)