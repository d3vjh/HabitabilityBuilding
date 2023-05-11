import math as m
import HabitabilityBuilding as hb

class Apartament:
    Text = 17  # 15-25
    Clo = 0.1  # Ropa 0-1.5
    Npersonas = 1  # 1-4
    Radiacion = 4033.3  # 4000-4400
    HumedadAir = 20  # 20-80%
    #constantes
    conductividad = 1.7  # Conductividad térmica hormigon
    grosor = 0.1  # Grosor hormigon

    def __init__(self, Text, Clo, Npersonas, Radiacion, conductividad, grosor, HumedadAir):
        self.Text = Text
        self.Clo = Clo
        self.Npersonas = Npersonas
        self.Radiacion = Radiacion
        self.conductividad = conductividad
        self.grosor = grosor
        self.HumedadAir = HumedadAir

    def Sedificio():
        pisos = 7
        apartamentos = 5
        lado = 44
        alto = 3
        apotema = 37.42
        # area prisma pentagonal
        Sedificio = 5*lado*(alto + (5/4)*apotema)
        return Sedificio/(pisos*apartamentos)  # m^2

    def U():
        # coeficiente de transmisión térmica
        return conductividad / grosor

    def QTotal():
        Tpiel = 33  # 33-37
        Spersona = 1.8
        n = 0.3  # eficiencia de absorción hormigon

        # fórmula del índice de vestimenta
        Icl = 0.155 * Clo ^ 0.425 * (1.0 / (1.0 + 0.09115 * m.sqrt(Spersona)))
        # convierto W
        TempPerson = ((Tpiel-Text) / Icl)*Npersonas

        # calor debidas a la radiación solar
        TempRadiacion = (Sapartament * Radiacion * n)/24

        # calor total
        return TempPerson + TempRadiacion

    def TempApartament():
        Sapartament = Sedificio()
        # transferencia de calor
        return Text + (QTotal() / (Sapartament * U()))



class Habitable (Apartament):

    def TransferenciaTemp():
        Spared=[51,34.5]#17x3 11.5x3  
        Stecho=[357,391,483]#17x21  17x23  21x23

#Rellenar switch 101...705 con:
        Stotal= Spared[0]+Stecho[0]*2 #pequeño apartament 201
        Stotal= Spared[0]+Spared[1]+Stecho[1]*2 #mediano apartament 202
        Stotal= Spared[1]*2+Stecho[2]*2 #grande apartament 203


        Stotal= Spared[0]+Stecho[0] #pequeño apartament 101
        Stotal= Spared[0]+Spared[1]+Stecho[1]#mediano apartament 102
        Stotal= Spared[1]*2+Stecho[2] #grande apartament 103

        #  ley de Fourier del calor
        return conductividad *Stotal*(TempApartament()-TempApartament())/grosor

    
    def Habitable():
        if HumedadAir >= 20 and HumedadAir <= 80:
            if TempApartament() >= 18.9 and TempApartament() <= 26.1:
                return True
            else:
                return False
        else:
            return False

    if __name__ == '__main__':
        print("La temperatura del apartamento es: ", TempApartament(), "°C")
