# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Bienvenue dans le jeu des Boules de Neige !
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Vous pouvez modifier ici les paramètres du jeu :

# Vitesse max de chute des boules de neiges (int, Default = 20)
vitesseMaxBoules = 20

# Moyenne de boules par secondes (float, Default = 1)
nombreSecEntreBoules = 1

# Nombre maximum de boules sur l'écran (int, Default = 5)
nombreMaxBoules = 5

# Rayon possible des boules de neige (list, Default = [4, 8, 16, 32, 64])
choixRayonBoules = [8, 16, 32, 64]

# Résolution du jeu en pixels ((int, int), Default = (1000, 600))
resolution = (1000,600)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ne pas modifier

for e in choixRayonBoules:
    assert e in [4, 8, 16, 32, 64], "Les rayons possibles sont 4, 8, 16, 32, 64"
assert 400 <= resolution[0] <= 1000 and resolution[1] == 600, "La largeur doit être entre 400 et 1000 pixels et la hauteur est de 600 pixels"
assert resolution[0] > 0 and resolution[1] > 0, "La résolution doit être positive"
assert vitesseMaxBoules > 0, "La vitesse max doit être positive"
assert nombreSecEntreBoules > 0, "Le nombre de boules par secondes doit être positif"