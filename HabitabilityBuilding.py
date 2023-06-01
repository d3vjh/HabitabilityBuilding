#!/bin/python3

import psycopg2, signal, os, sys, re
import networkx as nx
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import time


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
        
        self.q_temperature_individual = 0 # Temperatura individual, aislado del mundo
        self.q_temperature = 0 # Afectado por los vecinos -> Va en la BDD 

        self.q_heat_individual = 0
        self.q_heat = 0


    def addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)


    def addResidents(self, resident):
        if resident not in self.residents:
            self.residents.append(resident)

    def delResidents(self, resident):
        if resident in self.residents:
            self.residents.remove(resident)
        else:
            print("[!] Error, residente no encontrado! ")
            print(f'ID, del que llego a delResidents: {resident.k_person}')
            print(f'Nombre del que llego a delResidents: {resident.s_name}')
            input("")


    def getInfo(self):
        print(f'[+]==== Info del apartamento: {self.k_apartment}====[+]\n\n'
              f''
              f'[+] Es esHabitable: {self.b_is_habitable} \n'
              f'[+] Vecinos: \n')
        for neighbor in self.neighbors:
            print(f'\t[-] Número: {neighbor.k_apartment}')
            print(f'\t[-] Temperatura Individual: {neighbor.q_temperature_individual}')
            print(f'\t[-] Temperatura influenciada: {neighbor.q_temperature}')
            print(f'\t[-] Calor individual: {neighbor.q_heat_individual}')
            print(f'\t[-] Calor Influenciada: {neighbor.q_heat}')

        print(f'\n[+] Humedad del aire:  {self.q_air_humidity} \n'
              f'[+] Temperatura Individual: {self.q_temperature_individual} \n'
              f'[+] Temperatura Influenciada: {self.q_temperature} \n'
              f'[+] Calor Individual: {self.q_heat_individual} \n'
              f'[+] Calor Influenciada: {self.q_heat} \n'
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
        print(f'[!] Recomendación {Logic.esHabitable(self.k_apartment)} ')


    def getPerson(self, k_person):
        for person in self.residents:
            if person.k_person == k_person:
                return person 
        return None

    def getTemperatureNeighbors(self):
            TempVecinos = []
            for neighbor in self.neighbors:
                TempVecinos.append(neighbor.q_temperature_individual)
            return TempVecinos
                    



class Building:


    def __init__(self):
        self.Apartments = {}
        # Condiciones para un edicifio en Bogotá
        self.temp_exterior = 15 # 15-25
        self.q_radiaton = 4033.3  # 4000-4400 en bogota
        self.q_conductividad = 1.7  # Conductividad térmica hormigon
        self.grosor = 0.1  # Grosor hormigon
        self.superficie_Edificio = 312.871 # m^2


    def addApartment(self, k_apartment, q_air_humidity, s_apartment_material, q_number_of_bedrooms,
                     q_number_of_occupants, personClothing):
        if k_apartment not in self.Apartments:
            self.Apartments[k_apartment] = Apartment(k_apartment, q_air_humidity,
                                                         s_apartment_material, q_number_of_bedrooms, q_number_of_occupants,
                                                         personClothing)
        else:
            print("The apartment already exists")
            self.Apartments[k_apartment].getInfo()


    def getApartment(self, k_apartment):
        apt = self.Apartments[k_apartment]
        return apt


    def addNeighbor(self, k_apartment1, k_apartment2):
        if k_apartment1 in self.Apartments and k_apartment2 in self.Apartments:
            self.Apartments[k_apartment1].addNeighbor(self.getApartment(k_apartment2)) #intento cambio
            self.Apartments[k_apartment2].addNeighbor(self.getApartment(k_apartment1))



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
        
        for apartment in building.Apartments:
            # agrega el nodo correspondiente en el grafo
            apt = building.Apartments[apartment]
            
            G.add_node(apartment, number=apt.k_apartment, b_is_habitable=apt.b_is_habitable)
            
            # itera sobre los vecinos del apartamento actual
            for neighbor_number in apt.neighbors:
                # busca el nodo correspondiente en el grafo usando su número de apartamento
                neighbor_node = next((node for node in G.nodes() if G.nodes[node]['number'] == neighbor_number.k_apartment), None)
                
                # si se encontró el nodo, agrega la arista correspondiente
                if neighbor_node:
                    G.add_edge(apartment, neighbor_node)

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
    def updatePerson(k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity):
        print("")
        try:
            q = "UPDATE PERSON SET s_name = %s, s_last_name = %s, s_clothing_type = %s, s_activity = %s WHERE k_person = %s;"
            args = (s_name, s_last_name, s_clothing_type, s_activity, k_person,)
            db.executeQuery(q, args)
        except psycopg2.Error as e:
            print("[BDD] Error en la actualización de la persona: ", e)
            input("Press any key to continue...")



    @staticmethod
    def deletePerson(k_apartment, k_person):
        try:
            q = "DELETE FROM person WHERE k_person = %s;"
            args = (k_person,)
            db.executeQuery(q, args)
            # Agregar el resto de parámetros && la condición NOT NULL

            # DEBE llamar a addResidents()
            
            apt = building.Apartments[k_apartment]
            k_person = int(k_person) 

            resident = apt.getPerson(k_person)
#            print(resident)
#            print(apt.residents)
#            input("Test.... en deletePerson")
            apt.delResidents(resident)

            
            # Obtenemos el valor actual de ocupantes en el edificio
            q = "SELECT q_number_of_occupants FROM apartment WHERE k_apartment = %s"
            args = (k_apartment,)
            numAct = db.executeQuery(q, args)
            num = list(numAct)
            num = num[0][0]
#            print(num)
#            print(type(num))
            # Restamos en uno, el valor de q_number_of_occupants
            q = "UPDATE apartment SET q_number_of_occupants = %s WHERE k_apartment = %s"
            num -= 1
            args = (num, k_apartment,)
            db.executeQuery(q, args)

            building.Apartments[k_apartment].q_number_of_occupants -= 1

            
        except psycopg2.Error as e:
            print("[BDD] Error en la eliminación de la persona: ", e)
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
    def Menu_updatePerson():

        os.system("clear")

        print("[+] Actualizar Persona [+]") 

        k_apartment = int(input("[+] Ingrese el número del apartamento en el que se encuentra: "))
        while k_apartment not in building.Apartments:
            k_apartment = int(input("[!] El número de apartamento no existe, porfavor verifique de nuevo: "))

        apt = building.Apartments[k_apartment]
        
        print(f'Residentes del Apartamento N° {k_apartment}')
        for resident in apt.residents:
            print(f'\t[*] Nombre: {resident.s_name}')
            print(f'\t[*] Identificación: {resident.k_person}\n')

        k_person = int(input("[+] Ingrese el número de identificación de la persona: "))
        while not BDD.isPerson(k_person):    
            k_person = int(input("[+] Numero de identificación NO REGISTRADO, porfavor verifique de nuevo: "))
      
        resident = apt.getPerson(k_person)

        print(f'¿Que desea modificar?')

        print(f'[1] Nombre y Apellido')
        print(f'[2] Tipo de ropa')
        print(f'[3] Tipo de actividad')
        print(f'[4] Salir')


        while True:
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1:
                    s_name = input("[+] Ingrese el nombre de la persona: ")
                    while not re.match("^[A-Za-z]*$", s_name):
                        s_name = input("[!] Ingrese un nombre válido, sin números ni carácteres especiales: ")

                    s_last_name = input("[+] Ingrese el apellido de la persona: ")
                    while not re.match("^[A-Za-z]*$", s_last_name):
                        s_last_name =  input("[!] Ingrese un apellido válido, sin números ni carácteres especiales:")

                    resident.s_name = s_name
                    resident.s_last_name = s_last_name

                elif opc == 2:
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

                    resident.s_clothing_type = s_clothing_type


                elif opc == 3:
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

                    resident.s_activity = s_activity

                else:
                    Menu.initialMenu()
            except ValueError:
                print("[!] Debe ingresar un número entero válido.")
                input("Press any key to continue...")
                Menu.initialMenu()
            except KeyError:
                print("[!] La opción elegida no es válida.")
                input("Press any key to continue...")
                Menu.initialMenu()
 
            print(f'[+] {resident.s_name}')
            print(f'[+] {resident.s_last_name}')
            print(f'[+] {resident.k_apartment}')
            print(f'[+] {resident.s_clothing_type}')
            print(f'[+] {resident.s_activity}')
            input("Press any key to continue...")
            BDD.updatePerson(resident.k_person, resident.s_name, resident.s_last_name, resident.s_clothing_type, resident.k_apartment, resident.s_activity)
            
            Logic.run()
            Menu.initialMenu()
        




    @staticmethod
    def Menu_createPerson():
        os.system("clear")
    
        k_apartment = int(input("[+] Ingrese el número del apartamento en el que va a estar: "))
        while k_apartment not in building.Apartments:
            k_apartment = int(input("[!] El número de apartamento no existe, porfavor verifique de nuevo: "))

        k_person = int(input("[+] Ingrese el número de identificación de la persona: "))
        while BDD.isPerson(k_person):    
            k_person = int(input("[+] Numero de identificación ya ingresado, porfavor verifique de nuevo: "))
            
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

        Logic.run()
        Menu.initialMenu()
            # Ingrese el resto de valores 
       

    @staticmethod
    def Menu_deletePerson():
        os.system("clear")

        k_apartment = int(input("[+] Ingrese el número del apartamento en el que ya no va a residir: "))
        while k_apartment not in building.Apartments:
            k_apartment = int(input("[!] El número de apartamento no existe, porfavor verifique de nuevo: "))

        apt = building.Apartments[k_apartment]
        print(f'===[]Lista de residentes del {k_apartment}[]===')
        for resident in apt.residents:
            print(f'\t[*] Nombre: {resident.s_name}')
            print(f'\t[*] Identificación: {resident.k_person}\n')

        k_person = int(input("[+] Ingrese el número de identificación de la persona: "))
        while not BDD.isPerson(k_person):    
            k_person = int(input("[+] Numero de identificación NO REGISTRADO, porfavor verifique de nuevo: "))

        BDD.deletePerson(k_apartment, k_person)
        
        print(f'[√] Persona eliminada correctamente')
        input("Press any key to continue...")
        Logic.run()
        Menu.initialMenu()


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
        print("[3] Actualizar una persona de un apartamento")
        print("[4] Eliminar una persona de un apartamento")
        print("[5] Dibujar el Grafo")
        print("[9] Salir")


        while True:
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1:
                    Menu.Menu_getApartmentInfo()
                elif opc == 2:
                    Menu.Menu_createPerson()
                    Logic.run()
                elif opc == 3:
                    Menu.Menu_updatePerson()
                    Logic.run()
                elif opc == 4:
                    Menu.Menu_deletePerson()
                    Logic.run()
                elif opc == 5:
                    Logic.run()
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



class Logic():

    @staticmethod
    def run():
        
        for apt in building.Apartments:
            apartment = building.getApartment(apt)
            Logic.CalorIndividual(apartment.k_apartment)
            #print(f'CALOR Individual[{apartment.k_apartment}]: {Logic.CalorIndividual(apartment.k_apartment)} --- {apartment.q_heat_individual}')
            
        for apt in building.Apartments:
            apartment = building.getApartment(apt)
            #print(f'Temperatura Individual[{apartment.k_apartment}]: {Logic.TemperaturaIndividual(apartment.k_apartment)} ---- {apartment.q_temperature_individual}')
            Logic.TemperaturaIndividual(apartment.k_apartment)
        

        for apt in building.Apartments:
            apartment = building.getApartment(apt)
            #print(f'Guardar Calor: [{apartment.k_apartment}]: {Logic.GuardarCalor(apartment.k_apartment)}')
            Logic.GuardarCalor(apartment.k_apartment)
            #print("\n")

        for apt in building.Apartments:
            apartment = building.getApartment(apt)
            #print(f'Temp Total: [{apartment.k_apartment}]: {Logic.TempTotal(apartment.k_apartment)}')
            Logic.TempTotal(apartment.k_apartment)
            #print("\n")

        for apt in building.Apartments:
            apartment = building.getApartment(apt)
            Logic.esHabitable(apartment.k_apartment)


    

    @staticmethod
    def TempTotal(k_apartment): # Temperatura total CON transferencia

        apt = building.Apartments[k_apartment]
        # modificar Superficie a Apartamento
        if apt.q_number_of_bedrooms == 1: 
            superficie = 63
        elif apt.q_number_of_bedrooms == 2:
            superficie = 69
        elif apt.q_number_of_bedrooms == 3:
            superficie = 132

        try:
            temp = round(building.temp_exterior + apt.q_heat/(superficie * 17),3)

            #print(f'Temp desde TempTotal: {temp}')
            apt.q_temperature = temp
            return temp
        except:
            return None



    def GuardarCalor(k_apartment): # Se está comportando raro

        apt = building.Apartments[k_apartment]

        lista = Logic.TransferenciaCalor(k_apartment)
        sumLista = (sum(lista)) * -1
        #print(f'Lista: {lista}')
        #print(f'sumLista: {sumLista}')


        apt.q_heat = apt.q_heat_individual + sumLista

        i = 0
        for neighbor in apt.neighbors:
            neighbor.q_heat = neighbor.q_heat_individual + lista[i] #SUma
            i += 1
        
           # print(f'{neighbor.k_apartment}')
            #print(f'{neighbor.q_heat}')

        return apt.q_heat  




    @staticmethod
    def esHabitable(k_apartment):

        apt = building.Apartments[k_apartment]
        tempHumedad = round((apt.q_air_humidity / 10 )*10 , 3)
        

        Thumedad = {
            0: [25, 28],
            10: [35, 40],
            20: [20, 24],
            30: [19, 23],
            40: [18, 22],
            50: [24, 34],
            60: [16, 20],
            70: [20, 24],
            80: [14, 18],
            90: [13, 17],
            100: [12, 16]
        }
        
        TMinimo = Thumedad[apt.q_air_humidity][0]
        TMaximo = Thumedad[apt.q_air_humidity][1]



        if apt.q_air_humidity < 20:
            print("La humedad en el aire es muy baja, mantente hidratado")
        elif apt.q_air_humidity > 80:
            print("La humedad en el aire es muy alta, cuidese del moho")

        if TMinimo <= apt.q_temperature <= TMaximo:
            apt.b_is_habitable = True
        else:
            if apt.q_temperature > TMaximo: 
                if tempHumedad - TMaximo <= 1:
                    print("Baja la temperatura pintando de Blanco")
                else:
                    print("Compra Aire acondicionado")
            if apt.q_temperature < TMinimo:
                if apt.q_temperature - TMinimo >= -1:
                    print("Suba la temperatura pintando de Negro")
                else:
                    print("Compra un calentador")
            apt.b_is_habitable = False



    @staticmethod
    def CalorIndividual(k_apartment): # CALOR interno del apartamento sin transferencia
                
        apt = building.Apartments[k_apartment]

        Tactivity = {
            "Reposo": 37,
            "Ligera": 38,
            "Moderada": 39,
            "Intensa": 40
        }
        
        temperatura = 0 # Revisar
        Spersona = 1.8 # m^2
        n = 0.3  # eficiencia de absorción hormigon 0.2-0.4, cambia al pintar


        for resident in apt.residents:

            Tpiel = Tactivity[resident.s_activity]
 
            if resident.s_clothing_type == 'Casual':
                num_clothing = 1
                indice_vestimenta = 0.013811
            else:
                num_clothing = 0.2
                indice_vestimenta = 0.069689

            TempPerson = ((Tpiel - building.temp_exterior)/indice_vestimenta)
            temperatura += TempPerson # Revisar

        
        
        TempRadiacion = (building.superficie_Edificio * building.q_radiaton * n)/24 # Radiación -> Kw/d -> Kw/h   
        apt.q_heat_individual = temperatura + TempRadiacion
        return apt.q_heat_individual #Devuelve en Calor (Watts)
   

    @staticmethod
    def TemperaturaIndividual(k_apartment): # Calcula Temperatura C° idividual

        apt = building.Apartments[k_apartment]
            
        if apt.q_number_of_bedrooms == 1: 
            superficie = 63
        elif apt.q_number_of_bedrooms == 2:
            superficie = 69
        elif apt.q_number_of_bedrooms == 3:
            superficie = 132
        try:
            temperaturaInterna = round(building.temp_exterior + apt.q_heat_individual/(superficie * 17),3)
            apt.q_temperature_individual = temperaturaInterna
            return apt.q_temperature_individual
        except:
            return None

    @staticmethod
    def TransferenciaCalor(k_apartment): # Calor con transferencia

        apt = building.Apartments[k_apartment]

        piso = k_apartment // 100

        if apt.q_number_of_bedrooms == 1:
            size = "pequeño"
        elif apt.q_number_of_bedrooms == 2:
            size = "mediano"
        elif apt.q_number_of_bedrooms == 3:
            size = "grande"

        Scontacto = {
            "pequeño": {"pared": 51, "techo": 357, "piso": 357},
            "mediano": {"pared": 34.5, "techo": 391, "piso": 391},
            "grande": {"pared": 11.5, "techo": 483, "piso": 483},
        }
        Q = []
        i=0
        temperaturaVecinos = apt.getTemperatureNeighbors()
        for neighbor in apt.neighbors:
            posVecino = neighbor.k_apartment // 100
            if posVecino == piso:
                posicion = "pared"
            elif posVecino > piso:
                posicion = "techo"
            elif posVecino < piso:
                posicion = "piso"

            Stotal = Scontacto[size][posicion]

            total = round((building.q_conductividad * Stotal * (apt.q_temperature_individual - temperaturaVecinos[i]))/building.grosor, 1) #Formula de transferencia de Calor
                
            Q.append(total)
            i += 1
        return Q # Calor Que apt.k_apartment damos a los vecinos respectivamente




if __name__ == '__main__':


    BDD.loadApartments(building)
    BDD.loadNeighbors(building)
    BDD.loadResidents(building)
    Logic.run()



    Menu.initialMenu()


    #    bd = Building()
    #    BDD.loadNeighbors(bd)

#    os.system("kitty +kitten icat /home/d3vjh/Desktop/fondos/Wallpaper.jpg")
    

