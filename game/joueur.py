from math import sqrt, floor, sin, cos, atan2, pi

class Joueur:

    def __init__(self, maxPos, pos=[0,0], vector=[0,0]):
        self.pos = pos
        self.vector = vector
        self.maxPos = maxPos
        self.goRight = False
        self.goLeft = False
        self.isBreaking = False
        self.reloadEsquive = 0
        self.nombreVies = 3
        self.action = 'DN'
        self.image = f'/assets/Noel{self.action}.gif'

    def update(self):
        if self.action[1] == 'N':
            if self.goRight:
                self.moveRight()
            if self.goLeft:
                self.moveLeft()
            if self.isBreaking:
                self.breaking()
            if not self.goRight and not self.goLeft and not self.isBreaking and self.vector[0] != 0:
                self.vector[0] += 0.2 if self.vector[0] < 0 else -0.2
                if abs(self.vector[0]) < 0.25:
                    self.vector[0] = 0
        elif self.action[1] == 'E':
            self.vector[0] += 1 if self.vector[0] < 0 else -1
            if abs(self.vector[0]) <= 2:
                self.action = self.action[0]+'N'
                self.pos[1] -= 62 # 150 - 88 = 62, pour que l'image reste sur le sol
        # Translation de la position avec le vecteur
        if self.pos[0] < 0:
            self.vector[0] = abs(self.vector[0])
            self.action = 'D'+self.action[1]
        elif self.pos[0]+(88 if self.action[1] == 'N' else 150) > self.maxPos[0]:
            self.vector[0] = -abs(self.vector[0])
            self.action = 'G'+self.action[1]
        # if self.vector [0] > 0 and self.action != 'DN' and self.action[1] == 'N':
        #     self.action = 'DN'
        #     self.image = f'/assets/Noel{self.action}.gif'
        # elif self.vector [0] < 0 and self.action != 'GN' and self.action[1] == 'N':
        #     self.action = 'GN'
        #     self.image = f'/assets/Noel{self.action}.gif'
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]
        # Pour éviter des coordonées à cheval sur deux pixels
        self.pos[0] = floor(self.pos[0])
        self.pos[1] = floor(self.pos[1])
        if self.reloadEsquive > 0:
            self.reloadEsquive -= 1

    def moveLeft(self):
        self.vector[0] -= 1
        if self.vector[0] < -15:
            self.vector[0] = -15
        self.action = 'G'+self.action[1]

    def moveRight(self):
        self.vector[0] += 1
        if self.vector[0] > 15:
            self.vector[0] = 15
        self.action = 'D'+self.action[1]

    def breaking(self):
        self.vector[0] /= 2
        if -0.05 < self.vector[0] < 0.5:
            self.vector[0] = 0

    def esquive(self):
        if self.reloadEsquive == 0 and self.vector[0] != 0:
            self.reloadEsquive = 90
            if self.vector[0] > 0:
                self.vector[0] = 30
                self.action = 'DE'
            elif self.vector[0] < 0:
                self.vector[0] = -30
                self.action = 'GE'
            self.pos[1] += 62 # 150 - 88 = 62, pour que l'image reste sur le sol

    def inputs(self, actn: str, bol: bool):
        if actn == 'R':
            self.goRight = bol
        elif actn == 'L':
            self.goLeft = bol
        elif actn == 'B':
            self.isBreaking = bol

    def isOverlapping(self, other):
        # On modélise les boules par un cercle et le joueur par un ovale
        self_centre = self.getCentre()
        other_centre = other.getCentre()
        # On calcule l'angle entre les deux centres
        angle = atan2(other_centre[1]-self_centre[1], other_centre[0]-self_centre[0])
        # On calcule la distance entre les centre des deux objets
        distance = sqrt((self_centre[0]-other_centre[0])**2 + (self_centre[1]-other_centre[1])**2)
        # On retire les rayons des deux objets pour avoir la distance séparant les surafaces des deux objets
        distance -= other.getRayon() + self.getRayon(angle)
        if distance < 0:
            return True, distance
        return False, distance

    def getPos(self):
        return self.pos

    def getCentre(self):
        return [self.pos[0] + (88 if self.action[1] == 'N' else 150) / 2, self.pos[1] + (150 if self.action[1] == 'N' else 88) / 2]

    def getRayon(self, angle):
        # Le joueur est modélisé par un ovale
        return (44*75)/sqrt(((44 if self.action[1] == 'N' else 75)*sin(angle))**2 + ((75 if self.action[1] == 'N' else 44)*cos(angle))**2)

    def getVector(self):
        return self.vector

    def getAction(self):
        return self.action

    def getImage(self):
        return self.image

    def getReloadEsquive(self):
        return self.reloadEsquive

    def getVie(self):
        return self.nombreVies

    def perdreVie(self, nombreVies):
        self.nombreVies -= nombreVies
        self.nombreVies = max(0, self.nombreVies)

    def setImage(self):
        self.image = f'/assets/Noel{self.action}.gif'