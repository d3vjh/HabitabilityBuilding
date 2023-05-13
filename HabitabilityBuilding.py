#!/bin/python3

import psycopg2, signal, os, sys, time
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Database:
    __instance = None

    @staticmethod
    def getInstance():
        """Static access method to Singleton instance."""
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        """Virtually private constructor"""
        if Database.__instance is not None:
            raise Exception(
                "Another instance of this class already exists! Please use Database.getInstance() to access it.")
        else:
            Database.__instance = self
            self.connection = psycopg2.connect(
                host="localhost",
                database="habitable",  # This database must be updated later
                user="root",
                password="ballena12")

    def executeQuery(self, query, args=None):
        """Method to execute a query on the database."""
        cursor = self.connection.cursor()
        try:
            if args:
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            if cursor.description:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            cursor.close()
            return result
        except:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def closeConnection(self):
        """Method to close the database connection."""
        self.connection.close()

"""A global instance is created to access the database"""
db = Database.getInstance()

"""A global instance is created to access the Graph"""
G = nx.Graph()


"""Function to manage the output flow when Ctrl+C is pressed"""
def sig_handler(sig, frame):
        print("\n\n[!] Exiting ...")
        print("[!] Closing Instance with the database")
        print(" Bye! ")
        db.closeConnection()
        sys.exit(1)

signal.signal(signal.SIGINT, sig_handler)


class Apartment:
    def __init__(self, numberApartment, airHumidity, ambientAirTemperature, apartmentMaterial, roomQuantity,
                 personQuantity, isHabitable):
        self.numberApartment = numberApartment
        self.airHumidity = airHumidity
        self.ambientAirTemperature = ambientAirTemperature
        self.apartmentMaterial = apartmentMaterial
        self.roomQuantity = roomQuantity
        self.personQuantity = personQuantity
        self.neighbors = []
        self.isHabitable = isHabitable

    def addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def getInfo(self):
        print(f'[+]==== Info del apartamento: {self.numberApartment}====[+]\n\n'
              f''
              f'[+] Es Habitable: {self.isHabitable} \n'
              f'[+] Vecinos: {self.neighbors} \n'
              f'[+] Humedad del aire:  {self.airHumidity} \n'
              f'[+] Temperatura ambiental: {self.ambientAirTemperature} \n'
              f'[+] Material del apartamento: {self.apartmentMaterial} \n'
              f'[+] Tamaño del apartamento: {self.roomQuantity} \n'
              f'[+] Cantidad de personas: {self.personQuantity} \n')


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
            print("The apartment already exists")
            self.Apartments[numberApartment].getInfo()

    def addNeighbor(self, numberApartment1, numberApartment2):
        if numberApartment1 in self.Apartments and numberApartment2 in self.Apartments:
            self.Apartments[numberApartment1].addNeighbor(numberApartment2)
            self.Apartments[numberApartment2].addNeighbor(numberApartment1)



"""A global instance is created to access the Building""" 
building = Building()


class Person:
    def __init__(self, name, lastName, apartment, clothes):
        self.name = name
        self.lastName = lastName
        self.apartment = apartment
        self.clothes = clothes
        


class Graphic:
    
    @staticmethod
    def loadGraph():
        
        for i in building.Apartments:
            # agrega el nodo correspondiente en el grafo
            G.add_node(i, number=building.Apartments[i].numberApartment, isHabitable=building.Apartments[i].isHabitable)
            
            # itera sobre los vecinos del apartamento actual
            for neighbor_number in building.Apartments[i].neighbors:
                # busca el nodo correspondiente en el grafo usando su número de apartamento
                neighbor_node = next((node for node in G.nodes() if G.nodes[node]['number'] == neighbor_number), None)
                
                # si se encontró el nodo, agrega la arista correspondiente
                if neighbor_node:
                    G.add_edge(i, neighbor_node)

#        for node in G.nodes():
#            print(G.nodes[node]['number'])
#            print(G.nodes[node]['isHabitable'])
#            print(G.edges(node))
#            print("[+]")
        Graphic.viewGraph()

    def viewGraph():
        node_colors = ['green' if G.nodes[node]['isHabitable'] else 'red' for node in G.nodes()]
        pos = nx.spectral_layout(G)
        nx.draw(G, pos = pos, edge_color = 'white', with_labels=True, node_color=node_colors)
        plt.savefig('grafo.png', facecolor='#1A1B26')
        os.system("kitty +kitten icat /home/d3vjh/Documents/UD/HabitabilityBuilding/grafo.png")
        Graphic.clearGraph()

    def clearGraph():
        G.clear()
        plt.clf()

    

#    G.add_nodes_from([1, 2, 3, 4])
#    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

#    pos = nx.spring_layout(G, dim=3)

 ##   fig = plt.figure()
  #  ax = fig.add_subplot(projection='3d')
#
   # nx.draw_networkx_nodes(G, pos, ax=ax)
    #nx.draw_networkx_edges(G, pos, ax=ax)
     
#    plt.show()
    


class BDD:
#Create
    @staticmethod
    def createPerson(numApartment, n_name_person, n_lastname_person):
        try:
            q = "INSERT INTO person(k_id_apartment, n_name_person, n_lastname_person) VALUES (%s, %s, %s);"
            args = (numApartment, n_name_person, n_lastname_person)
            db.executeQuery(q, args)
            # Agregar el resto de parámetros && la condición NOT NULL
        except psycopg2.Error as e:
            print("[BDD] Error en la creación de la persona: ", e)
            input("Press any key to continue...")


#Read
    @staticmethod
    def loadApartments(build):
        try:
            result = db.executeQuery("SELECT k_apartment, q_air_humidity, q_ambient_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable FROM apartment ORDER BY k_apartment;")

            for i in range(len(result)):
                numberApartment = result[i][0]
                airHumidity = result[i][1]
                ambientAirTemperature = result[i][2]
                apartmentMaterial = result[i][3]
                roomQuantity = result[i][4]
                personQuantity = result[i][5]
                isHabitability = result[i][6]
                build.addApartment(int(numberApartment), airHumidity, ambientAirTemperature, apartmentMaterial,
                               roomQuantity,
                               personQuantity, isHabitability)
        except psycopg2.Error as e:
            print("[BDD] Error en la operación de base de datos:", e)
            input("Press any key to continue...")
        


    @staticmethod
    def loadNeighbors(build):
        try:
            result = db.executeQuery("SELECT k_apartment1, k_apartment2 FROM neighbor")
            for i in range(len(result)):
                numberApartment1 = result[i][0]
                numberApartment2 = result[i][1]
                build.addNeighbor(numberApartment1, numberApartment2)

        except psycopg2.Error as e:
            print("[BDD ldNeighbors] Error en la operación de base de datos:", e)
            input("Press any key to continue...")




class Menu:

    @staticmethod
    def Menu_createPerson():
        os.system("clear")
    
        numApartment = int(input("[+] Ingrese el número del apartamento en el que va a estar: "))
        while numApartment not in building.Apartments:
            numApartment = int(input("[!] El número de apartamento no existe, porfavor verifique de nuevo: "))
        n_name_person = input("[+] Ingrese el nombre de la persona: ")
        while not re.match("^[A-Za-z]*$", n_name_person):
            n_name_person = input("[!] Ingrese un nombre válido, sin números ni carácteres especiales: ")
        n_lastname_person = input("[+] Ingrese el apellido de la persona: ")
        while not re.match("^[A-Za-z]*$", n_lastname_person):
            n_lastname_person =  input("[!] Ingrese un apellido válido, sin números ni carácteres especiales:")

        BDD.createPerson(numApartment, n_name_person, n_lastname_person)
        Menu.initialMenu()
            # Ingrese el resto de valores 
       

    @staticmethod
    def Menu_getApartmentInfo():
        os.system("clear")
        numApartment = int(input("[+] Ingrese el número del apartamento que desea consultar: "))
        if numApartment not in building.Apartments:
            print("[!] El número de apartamento no existe, porfavor verifique de nuevo")
            input("Press any key to continue...")
        else:
            building.Apartments[numApartment].getInfo()
            input("Press any key to continue...")
        Menu.initialMenu()

    @staticmethod
    def Menu_getGraph():
        os.system("clear")
#        BDD.loadApartments(building)
        Graphic.loadGraph()
        input("Press any key to continue...")
        Menu.initialMenu()


        

    @staticmethod
    def initialMenu():
        os.system("clear")
        os.system("figlet \"Habitability Building\"")
        print("[1] Obtener información de un apartamento")
        print("[2] Agregar una persona a un apartamento")
        print("[3] Dibujar el Grafo")
        print("[9] Salir")


        while True:
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1:
                    Menu.Menu_getApartmentInfo()
                elif opc == 2:
                    Menu.Menu_createPerson()
                elif opc == 3:
                    Menu.Menu_getGraph()
                elif  opc == 9:
                    sys.exit(0)
            except ValueError:
                print("[!] Debe ingresar un número entero válido.")
                input("Press any key to continue...")
                Menu.initialMenu()
            except KeyError:
                print("[!] La opción elegida no es válida.")
                input("Press any key to continue...")
                Menu.initialMenu()




if __name__ == '__main__':
    BDD.loadApartments(building)
    BDD.loadNeighbors(building)
    Menu.initialMenu()

    #    bd = Building()
    #    BDD.loadNeighbors(bd)

#    os.system("kitty +kitten icat /home/d3vjh/Desktop/fondos/Wallpaper.jpg")
    

