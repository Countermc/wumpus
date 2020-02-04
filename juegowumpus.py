import random


class Game(object):

    def __init__(self, edges=[]):

        if edges:
            cueva = {}
            N = max([edges[i][0] for i in range(len(edges))])
            for i in range(N):
                exits = [edge[1] for edge in edges if edge[0] == i]
                cueva[i] = exits

        # Creamos un dodecaedromo estandar, se adjunta imagen con los bordes del dodecaedromo.
        else:

            cueva = {1: [2, 3, 4], 2: [1, 5, 6], 3: [1, 7, 8], 4: [1, 9, 10], 5: [2, 9, 11],
                    6: [2, 7, 12], 7: [3, 6, 13], 8: [3, 10, 14], 9: [4, 5, 15], 10: [4, 8, 16],
                    11: [5, 12, 17], 12: [6, 11, 18], 13: [7, 14, 18], 14: [8, 13, 19],
                    15: [9, 16, 17], 16: [10, 15, 19], 17: [11, 20, 15], 18: [12, 13, 20],
                    19: [14, 16, 20], 20: [17, 18, 19]}

        self.cueva = cueva

        self.threats = {}

        self.flechas = 5

        self.distancia = 2

        self.jugador_pos = -1

    def hab_seguras(self):
        """ Devuelve una lista de las habitaciones que no contienen threats
        """
        return list(set(self.cueva.keys()).difference(self.threats.keys()))

    def busqueda_inicial(self, source, target, max_prof=5):

        # Valores iniciales.
        graph = self.cueva
        prof = 0

        def busqueda(stack, visited, target, prof):
            if stack == []:
                return False, -1
            if target in stack:
                return True, prof
            visited = visited + stack
            stack = list(set([graph[v][i] for v in stack for i in range(len(graph[v]))]).difference(visited))
            prof += 1
            if prof > max_prof:
                return False, prof
            else:
                return busqueda(stack, visited, target, prof)

        return busqueda([source], [], target, prof)

    def poblacion(self):
        """ Añade la población del juego.
        """
        for threat in ['murcielago', 'murcielago', 'pozo', 'pozo', 'wumpus', 'oro']:
            # en el tablero tendremos 2 murcielagos, 2 pozos, 1 wumpu y 1 lingote
            pos = random.choice(self.hab_seguras())
            self.threats[pos] = threat
        self.jugador_pos = random.choice(self.hab_seguras())

    def entradas_teclado(self):
        """ Recogemos las entradas de teclado
        """
        while 1:

            entrada = input("Disparas o te mueves (D-M)? ")
            try:  # Nos aseguramos que el jugador selecciona una acción valida
                mode = str(entrada).lower()  # Convertimos cualquier valor del teclado en minuscula
                assert mode in ['d', 'm']  # comparamos el valor con lo que tenemos en la lista
                break
            except (ValueError, AssertionError):
                print("No has introducido un valor correcto: elige 'D' para disparar o 'M' para mover ")

        while 1:
            entrada = input("¿A donde?")
            try:
                target = int(entrada)
            except ValueError:
                print("No es un valor válido.")
                continue

            if mode == 'm':
                try:
                    assert target in self.cueva[self.jugador_pos]
                    break
                except AssertionError:
                    print("No puedes acceder por ahí, por favor elige una habitación correcta")

            elif mode == 'd':
                try:  # Cuando disparamos, la maxima distancia serán dos tunels.
                    bi = self.busqueda_inicial(self.jugador_pos, target)
                    assert bi[0] == True
                    break
                except AssertionError:
                    if bi[1] == -1:
                        print("No has hecho un buen disparo, tu flecha se va en una dirección aleatoria.")
                        target = random.choice(self.cueva.keys())
                    if bi[1] > self.distancia:  # El objetivo está demasiado lejos.
                        print("Así no vas a acertar nunca.")
        return mode, target

    def advertencias(self, threath):

        if threath == 'murcielago':
            print("Escuchas unos ruidos")
        elif threath == 'pozo':
            print("Sientes una fria brisa muy cerca de ti")
        elif threath == 'wumpus':
            print("Hay un olor terrible, muy cerca tuya.")
        elif threath == 'oro':
            print("Te ha parecido ver un destello, pero no sabes de donde ha venido")

    def disparos(self, Hab_pos):
        """ Controlamos los disparos en una habitación
        """
        print("Disparas una flecha hacia {}...".format(Hab_pos))
        self.flechas -= 1
        threat = self.threats.get(Hab_pos)
        if threat in ['murcielago', 'wumpus']:
            del self.threats[Hab_pos]
            if threat == 'wumpus':
                print("GENIAL!!!, matastes al wumpus!")
                return -1
            elif threat == 'murcielago':
                print("Ohhh, has matado un murcielago.")
        elif threat in ['pozo', None]:
            print("La flecha se perdió en la oscuridad.")

        if self.flechas < 1:
            print("Tu carcaj está vacio.")
            return -1

        # Si tu disparo acaba en en otra habitación que no esté el Wumpus, el wumpus tiene un 75% de probabilidad de
        # moverse a una casilla adyacente.
        if random.random() < 0.75:
            for Hab_pos, threat in self.threats.items():
                if threat == 'wumpus':
                    wumpus_pos = Hab_pos
            nueva_pos = random.choice(list(set(self.cueva[wumpus_pos]).difference(self.threats.keys())))
            del self.threats[Hab_pos]
            self.threats[nueva_pos] = 'wumpus'
            if nueva_pos == self.jugador_pos:
                print("Wumpus entra en la habitación y te mata!")
                return -1

        return self.jugador_pos

    def Hab_entrada(self, Hab_pos):

        print("Estas entrando en la habitación {}...".format(Hab_pos))

        if self.threats.get(Hab_pos) == 'murcielago':
            print("Te atacan unos murcielagos, el miedo y la confusión te hacen correr hasta una habitación aleatoria.")
            new_pos = random.choice(self.hab_seguras())
            return self.Hab_entrada(new_pos)
        elif self.threats.get(Hab_pos) == 'wumpus':
            print("Wumpus te comió.")
            return -1
        elif self.threats.get(Hab_pos) == 'pozo':
            print("Te has caido en un pozo.")
            return -1
        elif self.threats.get(Hab_pos) == 'oro':
            print("Hurra!!! Has encontrado el lingote de oro. Has ganado la partida.")
            return -1

        # Las habitaciones seguras, nos dan información de los threats de las habitaciones adyacentes
        for i in self.cueva[Hab_pos]:
            self.advertencias(self.threats.get(i))

        return Hab_pos

    def motor(self):

        print("EL JUEGO DEL WUMPUS")
        print("===============")
        print()
        self.poblacion()
        self.Hab_entrada(self.jugador_pos)

        while 1:

            print("Estas en la habitación {}.".format(self.jugador_pos), end=" ")
            print("Tienes tres habitaciones a elegir:  {0}  {1}  {2}".format(*self.cueva[self.jugador_pos]))

            entrada = self.entradas_teclado()  # El jugador elige disparar o mover
            print()
            if entrada[0] == 'm':  # Movmiento.
                target = entrada[1]
                self.jugador_pos = self.Hab_entrada(target)
            elif entrada[0] == 'd':  # Disparo.
                target = entrada[1]
                self.jugador_pos = self.disparos(target)

            if self.jugador_pos == -1:
                break

        print()
        print("Game over!")


if __name__ == '__main__':
    GW = Game()
    GW.motor()
