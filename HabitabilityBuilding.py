#!/bin/python3

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
        self.neighbors = []
        self.isHabitability = True

    def addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def getInfo(self):
        print(f'[+]==== Info del apartamento: {self.numberApartment}====[+]\n\n'
              f''
              f'[+] Es Habitable: {self.isHabitability} \n'
              f'[+] Vecinos: {self.neighbors} \n'
              f'[+] Humedad del aire:  {self.airHumidity} \n'
              f'[+] Temperatura ambiental: {self.ambientAirTemperature} \n'
              f'[+] Material del apartamento: {self.apartmentMaterial} \n'
              f'[+] Tamaño del apartamento: {self.roomQuantity} \n'
              f'[+] Cantidad de personas: {self.personQuantity} \n'
              f'[+] Material de la ropa: {self.personClothing}\n')


class Building:
    def __init__(self):
        self.Apartments = {}

    def addApartment(self, numberApartment, airHumidity, ambientAirTemperature, apartmentMaterial, roomQuantity,
                     personQuantity, personClothing):
        if numberApartment not in self.Apartments:
            self.Apartments[numberApartment] = Apartment(numberApartment, airHumidity, ambientAirTemperature,
                                                         apartmentMaterial, roomQuantity, personQuantity,
                                                         personClothing)
        else:
            print("El apartamento ya existe")
            self.Apartments[numberApartment].getInfo()

    def addNeighbor(self, numberApartment1, numberApartment2):
        if numberApartment1 in self.Apartments and numberApartment2 in self.Apartments:
            self.Apartments[numberApartment1].addNeighbor(numberApartment2)
            self.Apartments[numberApartment2].addNeighbor(numberApartment1)


class BDD:

    @staticmethod
    def loadApartments(build):
        file = open("Apartments.txt", "r")
        content = file.readlines()
        for line in content:
            apartment = line.split('\t')
            numberApartment = apartment[0]
            airHumidity = apartment[1]
            ambientAirTemperature = apartment[2]
            apartmentMaterial = apartment[3]
            roomQuantity = apartment[4]
            personQuantity = apartment[5]
            personClothing = apartment[6]

            build.addApartment(int(numberApartment), airHumidity, ambientAirTemperature, apartmentMaterial, roomQuantity,
                            personQuantity, personClothing)

        file.close()

    @staticmethod
    def loadNeighbors(build):
        file = open("Neighbors.txt", "r")
        content = file.readlines()
        for line in content:
            neighbor = line.split('\t')
            numberApartment1 = neighbor[0]
            numberApartment2 = neighbor[1]
            build.addNeighbor(int(numberApartment1), int(numberApartment2))
        file.close()


if __name__ == '__main__':

    bd = Building()
    BDD.loadApartments(bd)
    BDD.loadNeighbors(bd)

    bd.Apartments[101].getInfo()

