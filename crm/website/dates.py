# Chaîne de caractères représentant l'heure
heure_string = "7:00 p.m"

# Diviser la chaîne en composants
heures, minutes_ampm = heure_string.split(":")
minutes, am_pm = minutes_ampm.split()

# Convertir les heures en entier
heures = int(heures)

# Ajuster l'heure pour le format PM
if am_pm.lower() == "p.m" and heures < 12:
    heures += 12

# Créer un objet time
objet_time = "{:02d}:{:02d}".format(heures, int(minutes))

# Imprimer l'objet time
print(objet_time)
