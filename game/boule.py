from random import choice

class Boule:

    def __init__(self, maxPos, maxSpeed, pos=[0,0], vector=[0,0], rayon=16):
        self.rayon = rayon
        self.pos = pos
        self.vector = vector
        self.maxPos = maxPos
        self.maxSpeed = maxSpeed
        self.image = f'/assets/boule{self.rayon}.gif'

    def update(self):
        if self.pos[0] < 0:
            self.vector[0] = abs(self.vector[0]*0.75)
        elif self.pos[0]+self.rayon*2 > self.maxPos[0]:
            self.vector[0] = -abs(self.vector[0]*0.75)
        # La balle atteint le sol
        if self.pos[1]+2*self.rayon > self.maxPos[1]:
            # On rebondit avec le vecteur symétrique sans modifier pour être sur que la balle repasse au-dessus de la limite
            self.pos[0] += self.vector[0]
            self.pos[1] -= self.vector[1]
            # La balle va moins vite après le rebond
            self.vector[1] *= -0.75
            self.vector[0] *= 0.75
            # La taille est réduite
            self.rayon = int(self.rayon/2)
            self.image = f'/assets/boule{self.rayon}.gif'
            # On repositionne bien la balle, car l'anchor est en haut à gauche donc le changement de taille n'est pas beau
            self.pos[0] += self.rayon
            self.pos[1] += self.rayon
            return 1
        # Translation de la position avec le vecteur
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]
        self.vector[1] = min(self.vector[1]+self.maxSpeed/100, self.maxSpeed)

    def getPos(self):
        return self.pos

    def getCentre(self):
        return [self.pos[0]+self.rayon, self.pos[1]+self.rayon]

    def getVector(self):
        return self.vector

    def getImage(self):
        return self.image

    def getRayon(self):
        return self.rayon