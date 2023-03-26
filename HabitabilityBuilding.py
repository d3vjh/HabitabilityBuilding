#!/bin/python3

class Building:
    def __init__(self, height, num_apartment, solarRadiation):
        self.height = 7
        self.num_apartment = 4
        self.apartments = []
        self.solarRadiation = 0

    def get_rooms(self):
        return self.rooms


class Apartment:
    def __init__(self, numberApartment, airHumidity, ambientAirTemperature, apartmentMaterial, roomQuantity,
                 personQuantity, personClothing):
        self.numberApartment = numberApartment
        self.airHumidity = airHumidity
        self.ambientAirTemperature = ambientAirTemperature
        self.apartmentMaterial = apartmentMaterial
        self.roomQuantity = roomQuantity
        self.personQuantity = personQuantity
        self.personClothing = personClothing

    def getNumberApartment(self):
        return self.numberApartment

    def getAirHumidity(self, numberApartment):
        return apartments

    def

if __name__ == '__main__':
    file = open("Build.txt", "r")
    content = file.readlines()

    for line in content:
        Habitation = line.split('\t')
        piso = Habitation[0]
        Numero = Habitation[1]
        NumHabitaciones = Habitation[2]
        print(piso, Numero, NumHabitaciones)

    file.close()

    print("Hello World")
