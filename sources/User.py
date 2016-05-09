class User:
    
    def __init__(self,nom,prenom,email,mdp,adresse,promo):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.adresse = adresse
        self.promo = promo
    
    def setLatLon(self,lat,lon):
        self.lat = lat
        self.lon = lon