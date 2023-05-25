#!/bin/python3

import psycopg2, signal, os, sys, re
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
                database="primeraprueba",  # This database must be updated later
                user="postgres",
                password="password")

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
    def __init__(self, k_apartment, q_air_humidity, s_apartment_material, q_number_of_bedrooms,
                 q_number_of_occupants, b_is_habitable):
        self.k_apartment = k_apartment
        self.q_air_humidity = q_air_humidity
        self.s_apartment_material = s_apartment_material
        self.q_number_of_bedrooms = q_number_of_bedrooms
        self.q_number_of_occupants = q_number_of_occupants
        self.neighbors = []
        self.residents = []
        self.b_is_habitable = b_is_habitable

    def addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)


    def addResidents(self, resident):
        if resident not in self.residents:
            self.residents.append(resident)


    def getInfo(self):
        print(f'[+]==== Info del apartamento: {self.k_apartment}====[+]\n\n'
              f''
              f'[+] Es Habitable: {self.b_is_habitable} \n'
              f'[+] Vecinos: {self.neighbors} \n'
              f'[+] Humedad del aire:  {self.q_air_humidity} \n'
              f'[+] Material del apartamento: {self.s_apartment_material} \n'
              f'[+] Tamaño del apartamento: {self.q_number_of_bedrooms} \n'
              f'[+] Cantidad de personas: {self.q_number_of_occupants} \n'
              f'[+] Personas residentes:')
        for person in self.residents:
            print(f'\t[-] Id: {person.k_person} \n'
                  f'\t[-] Nombre: {person.s_name}\n'
                  f'\t[-] Apellido: {person.s_last_name}\n'
                  f'\t[-] Ropa: {person.s_clothing_type}\n'
                  f'\t[-] Actividad: {person.s_activity}\n')


class Building:
    def __init__(self):
        self.Apartments = {}

    def addApartment(self, k_apartment, q_air_humidity, s_apartment_material, q_number_of_bedrooms,
                     q_number_of_occupants, personClothing):
        if k_apartment not in self.Apartments:
            self.Apartments[k_apartment] = Apartment(k_apartment, q_air_humidity,
                                                         s_apartment_material, q_number_of_bedrooms, q_number_of_occupants,
                                                         personClothing)
        else:
            print("The apartment already exists")
            self.Apartments[k_apartment].getInfo()

    def addNeighbor(self, k_apartment1, k_apartment2):
        if k_apartment1 in self.Apartments and k_apartment2 in self.Apartments:
            self.Apartments[k_apartment1].addNeighbor(k_apartment2)
            self.Apartments[k_apartment2].addNeighbor(k_apartment1)



"""A global instance is created to access the Building""" 
building = Building()


class Person:
    def __init__(self, k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity):

        self.k_person = k_person
        self.s_name = s_name
        self.s_last_name = s_last_name
        self.s_clothing_type = s_clothing_type
        self.k_apartment = k_apartment
        self.s_activity = s_activity
        


class Graphic:
    
    @staticmethod
    def loadGraph():
        
        for i in building.Apartments:
            # agrega el nodo correspondiente en el grafo
            G.add_node(i, number=building.Apartments[i].k_apartment, b_is_habitable=building.Apartments[i].b_is_habitable)
            
            # itera sobre los vecinos del apartamento actual
            for neighbor_number in building.Apartments[i].neighbors:
                # busca el nodo correspondiente en el grafo usando su número de apartamento
                neighbor_node = next((node for node in G.nodes() if G.nodes[node]['number'] == neighbor_number), None)
                
                # si se encontró el nodo, agrega la arista correspondiente
                if neighbor_node:
                    G.add_edge(i, neighbor_node)

#        for node in G.nodes():
#            print(G.nodes[node]['number'])
#            print(G.nodes[node]['b_is_habitable'])
#            print(G.edges(node))
#            print("[+]")
        Graphic.viewGraph()

    def viewGraph():
        node_colors = ['green' if G.nodes[node]['b_is_habitable'] else 'red' for node in G.nodes()]
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

    @staticmethod
    def isPerson(k_person):
        try:
            q = "SELECT k_person FROM person WHERE k_person = %s"
            args = (k_person,)
            result = db.executeQuery(q, args)
            if result:
                return True
            else:
                return False
        except:
            return False
#Create
    @staticmethod
    def createPerson(k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity):
        try:
            q = "INSERT INTO person(k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity) VALUES (%s, %s, %s, %s, %s, %s);"
            args = (k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity)
            db.executeQuery(q, args)
            # Agregar el resto de parámetros && la condición NOT NULL

            # DEBE llamar a addResidents()
            person = Person(k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity)
            building.Apartments[k_apartment].addResidents(person)

            
            # Obtenemos el valor actual de ocupantes en el edificio
            q = "SELECT q_number_of_occupants FROM apartment WHERE k_apartment = %s"
            args = (k_apartment,)
            numAct = db.executeQuery(q, args)
            num = list(numAct)
            num = num[0][0]
            print(num)
            print(type(num))
            # Aumentamos en uno, el valor de q_number_of_occupants
            q = "UPDATE apartment SET q_number_of_occupants = %s WHERE k_apartment = %s"
            num += 1
            args = (num, k_apartment,)
            db.executeQuery(q, args)

            building.Apartments[k_apartment].q_number_of_occupants += 1




            
        except psycopg2.Error as e:
            print("[BDD] Error en la creación de la persona: ", e)
            input("Press any key to continue...")


#Read
    @staticmethod
    def loadApartments(build):
        try:
            result = db.executeQuery("SELECT k_apartment, q_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable FROM apartment ORDER BY k_apartment;")

            for i in range(len(result)):
                k_apartment = result[i][0]
                q_air_humidity = result[i][1]
                s_apartment_material = result[i][2]
                q_number_of_bedrooms = result[i][3]
                q_number_of_occupants = result[i][4]
                b_is_habitable = result[i][5]
                build.addApartment(int(k_apartment), q_air_humidity, s_apartment_material,
                                    q_number_of_bedrooms, q_number_of_occupants, b_is_habitable)
        except psycopg2.Error as e:
            print("[BDD] Error en la operación de base de datos:", e)
            input("Press any key to continue...")
        


    @staticmethod
    def loadNeighbors(build):
        try:
            result = db.executeQuery("SELECT k_apartment1, k_apartment2 FROM neighbor")
            for i in range(len(result)):
                k_apartment1 = result[i][0]
                k_apartment2 = result[i][1]
                build.addNeighbor(k_apartment1, k_apartment2)

        except psycopg2.Error as e:
            print("[BDD ldNeighbors] Error en la operación de base de datos:", e)
            input("Press any key to continue...")


    @staticmethod
    def loadResidents(build):

        for i in build.Apartments:
            numApartment = int(build.Apartments[i].k_apartment)
            q = "SELECT k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity  FROM person WHERE k_apartment = %s"
            args = (numApartment,)
            result = db.executeQuery(q, args)            
            if result:
                for j in range(len(result)):
                    k_person = result[j][0]
                    s_name = result[j][1]
                    s_last_name = result[j][2]
                    s_clothing_type = result[j][3]
                    k_apartment = result[j][4]
                    s_activity = result[j][5]
                    person = Person(k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity)
                    build.Apartments[i].addResidents(person)
            del result
            




class Menu:

    @staticmethod
    def Menu_createPerson():
        os.system("clear")
    
        k_apartment = int(input("[+] Ingrese el número del apartamento en el que va a estar: "))
        while k_apartment not in building.Apartments:
            k_apartment = int(input("[!] El número de apartamento no existe, porfavor verifique de nuevo: "))

        k_person = input("[+] Ingrese el número de identificación de la persona: ")
        while BDD.isPerson(k_person):    
            k_person = input("[+] Numero de identificación ya ingresado, porfavor verifique de nuevo: ")
            
        s_name = input("[+] Ingrese el nombre de la persona: ")
        while not re.match("^[A-Za-z]*$", s_name):
            s_name = input("[!] Ingrese un nombre válido, sin números ni carácteres especiales: ")

        s_last_name = input("[+] Ingrese el apellido de la persona: ")
        while not re.match("^[A-Za-z]*$", s_last_name):
            s_last_name =  input("[!] Ingrese un apellido válido, sin números ni carácteres especiales:")
        
        clothing_type = {
                '1' : 'Casual',
                '2' : 'Desnudo'
                }
        print("[+] Selecciona el tipo de ropa: ")
        print(f'\t1. Casual\n' 
              f'\t2. Desnudo\n')
        s_clothing_type = input("[$]> ")
        while s_clothing_type not in clothing_type:
            s_clothing_type = input("[!] Ingrese una opción válida Porfavor: ")
        
        s_clothing_type = clothing_type[s_clothing_type]

        activity = {
                '1' : 'Reposo',
                '2' : 'Ligera',
                '3' : 'Moderada',
                '4' : 'Intensa'
                }
        print("[+] Selecciona la actividad a realizar: ")
        print(f'\t1. Reposo\n'
              f'\t2. Ligera\n'
              f' \t3. Moderada\n'
              f'  \t4. Intensa\n')
        s_activity= input("[$]> ")
        while s_activity not in activity:
            s_activity= input("[!] Ingrese una opción válida Porfavor: ")
        
        s_activity = activity[s_activity]



        BDD.createPerson(k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity)
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
    BDD.loadResidents(building)
    Menu.initialMenu()

    #    bd = Building()
    #    BDD.loadNeighbors(bd)

#    os.system("kitty +kitten icat /home/d3vjh/Desktop/fondos/Wallpaper.jpg")
    

