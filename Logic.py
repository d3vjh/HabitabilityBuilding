import math as m
import HabitabilityBuilding as bd


class Edificio:
    # constantes
    conductividad = 1.7  # Conductividad térmica hormigon
    grosor = 0.1  # Grosor hormigon

    def __init__(self, Text=None, Radiacion=None, HumedadAir=None):
        self.Text = Text
        self.Radiacion = Radiacion
        self.HumedadAir = HumedadAir

        if Text is None and Radiacion is None and HumedadAir is None:
            self.Constructor2()

    # Condiciones Edificio de bogota
    def Constructor2(self):
        self.Text = 17  # 15-25
        self.Radiacion = 4033.3  # 4000-4400
        self.HumedadAir = 70  # 20-80%

    @property
    def Sapartament(self):
        pisos = 7
        apartamentos = 5
        lado = 44
        alto = 3
        apotema = 37.42
        # area prisma pentagonal
        Sedificio = 5*lado*(alto + (5/4)*apotema)
        return round(Sedificio/(pisos*apartamentos), 3)  # m^2

    @property
    def U(self):
        # coeficiente de transmisión térmica
        return self.conductividad / self.grosor

    def TransferenciaTemp(self, apartamento, vecinos, Tapartament, Tvecino):

        ziseApartamento = int(str(apartamento)[-1])
        if ziseApartamento == 1 or ziseApartamento == 5:
            size = "pequeño"
        elif ziseApartamento == 2 or ziseApartamento == 4:
            size = "mediano"
        elif ziseApartamento == 3:
            size = "grande"

        piso = int(str(apartamento)[0])

        Scontacto = {
            "pequeño": {"pared": 51, "techo": 357, "piso": 357},
            "mediano": {"pared": 34.5, "techo": 391, "piso": 391},
            "grande": {"pared": 11.5, "techo": 483, "piso": 483},
        }

        Q = []
        for vecino in vecinos:

            Pvecino = int(str(vecino)[0])
            if Pvecino == piso:
                posicion = "pared"
            elif Pvecino > piso:
                posicion = "techo"
            elif Pvecino < piso:
                posicion = "piso"

            Stotal = Scontacto[size][posicion]
            #  ley de Fourier del calor
            Q.append(round(self.conductividad * Stotal *
                     (Tapartament-Tvecino)/self.grosor, 1))

        return Q
        


class Apartament():
    def __init__(self, Edificio, Clo=None, Npersonas=None, Activity=None):
        self.Edificio = Edificio
        self.Clo = Clo
        self.Npersonas = Npersonas
        self.Activity = Activity

        if Clo is None and Npersonas is None and Activity is None:
            self.Constructor2()

    # Condiciones Edificio de bogota
    def Constructor2(self):
        self.Clo = 1  # Ropa 0.1-1
        self.Npersonas = 1  # 1-4
        self.Activity = "ligera"

    def QTotal(self):
        Tactivity = {
            "reposo": 36,
            "ligera": 37,
            "moderada": 38,
            "intensa": 39
        }
        Tpiel = Tactivity[self.Activity]
        Spersona = 1.8
        n = 0.3  # eficiencia de absorción hormigon 0.2-0.4, cambia al pintar

        # fórmula del índice de vestimenta
        if self.Clo < 0.1:
            self.Clo = 0.1  # valor minimo
        Icl = 0.155 * self.Clo ** 0.425 * \
            (1.0 / (1.0 + 0.09115 * m.sqrt(Spersona)))
        # convierto W
        TempPerson = ((Tpiel-self.Edificio.Text) / Icl)*self.Npersonas

        # calor debidas a la radiación solar
        TempRadiacion = (self.Edificio.Sapartament *
                         self.Edificio.Radiacion * n)/24

        # calor total
        return TempPerson + TempRadiacion

    @property
    def TempApartament(self):
        # transferencia de calor
        return round(self.Edificio.Text + (self.QTotal() / (self.Edificio.Sapartament * self.Edificio.U)), 3)

    def Habitable(self):
        self.Edificio.HumedadAir = round(self.Edificio.HumedadAir/10)*10
        TempApartament = self.TempApartament
        print("La temperatura del apartamento es: ", TempApartament, "°C")
        Thumedad = {
            0: [25, 28],
            10: [24, 27],
            20: [20, 24],
            30: [19, 23],
            40: [18, 22],
            50: [17, 21],
            60: [16, 20],
            70: [15, 19],
            80: [14, 18],
            90: [13, 17],
            100: [12, 16]
        }
        Tmin = Thumedad[self.Edificio.HumedadAir][0]
        Tmax = Thumedad[self.Edificio.HumedadAir][1]

        if self.Edificio.HumedadAir < 20:
            print("la humedad en el aire es muy baja, mantente hidratado")
        elif self.Edificio.HumedadAir > 80:
            print("la humedad en el aire es muy alta, cuidate del moho")

        if Tmin <= self.TempApartament <= Tmax:
            return True
        else:
            if TempApartament > Tmax:
                if ((TempApartament - Tmax) <= 1):
                    print("baja la temperatura, pintando de blanco")
                else:
                    print("compra aire acondicionado")
            if TempApartament < Tmin:
                if TempApartament-Tmin >= -1:
                    print("sube la temperatura, pintando de negro")
                else:
                    print("compra calentador")
            return False


if __name__ == '__main__':
    e = Edificio()
    apt101 = Apartament(e, 0.1, 1, "reposo") #actual
    apt201 = Apartament(e, 1, 1, "reposo")
    # print("El apartamento es habitable: ", apt101.Habitable())
    # print("El apartamento es habitable: ", apt102.Habitable())

    bd.BDD.loadApartments(bd.building)
    bd.BDD.loadNeighbors(bd.building)

    info_Apartamentos = bd.building.Apartments
    Apartamentos = list(set(info_Apartamentos.keys()))
    for apartamento in Apartamentos:
        vecinos = bd.building.Apartments[apartamento].neighbors
        Q_new=e.TransferenciaTemp(apartamento, vecinos,
                            apt101.TempApartament, apt201.TempApartament)
        
