#!/bin/python3

'''
-> El edificio va a tener 7 pisos
-> Por cada piso va a tener 4 habitaciones -> No. habitaciones 1=1 2=2 1=3
-> Material ladrillo común
-> Temperatura
-> temperaturaAmbiente, temperaturaHabitación, materialPared, humedadAire, cantPersonas, capacidad
'''


class Building:
    def __init__(self, height, num_rooms):
        self.height = 7
        self.num_rooms = 4
        self.rooms = []

    def get_rooms(self):
        return self.rooms


class Room:
    def __init__(self, floor, number, num_rooms, temperaturaAmbiente, temperaturaHabitación, materialPared, cantPersonas):
        self.floor = floor
        self.number = number
        self.num_rooms = num_rooms
        self.temperaturaAmbiente
        self.temperaturaHabitacion
        self.materialPared
        self.humedadAire
        self.cantPersonas


    def get_floor(self):
        return self.floor

    def get_number(self):
        return self.number

    def get_num_rooms(self):
        return self.num_rooms

    def get_room_temperature(self):
        return self.temperaturaHabitacion

    def get_material_wall(self):
        return self.materialPared

    def get_amount_of_people(self):
        return self.cantPersonas




if __name__ == '__main__':
    print("Hello World")
