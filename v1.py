# Installer python : https://www.python.org/downloads/

# Installer les librairies nécessaires :
# Ouvrir l'invite de commande (cmd)
# Executer les deux commandes :
    # pip install win10toast
    # pip install pyhoneygain



from pyHoneygain import HoneyGain
from win10toast import ToastNotifier
import platform


def pot_honeygain(email:str, mdp:str):
    try:
        user = HoneyGain()
        # Connexion
        user.login(email, mdp)
        # Ouverture du pot quotidien
        pot = user.open_honeypot()
        # Si on est sur Windows on affiche la notification sinon on affiche dans la console
        if platform.system() == "Windows":
            # Si le pot est ouvert pour la première fois dans la journée
            if pot['success'] == True:
                return ToastNotifier().show_toast('Ouverture pot Honeygain', f"Vous venez de gagner {pot['credits']['credits']} credits !", duration=10, icon_path='')
            # Sinon
            elif pot['success'] == False:
                return ToastNotifier().show_toast('Ouverture pot Honeygain', f"Vous avez déjà ouvert votre pot aujourd'hui, il vous a rapporté {user.stats_today()['winning']['credits']} credits !", duration=10, icon_path='')
        else:
            # Si le pot est ouvert pour la première fois dans la journée
            if pot['success'] == True:
                return print(f"Vous venez de gagner {pot['credits']['credits']} credits !")
            # Sinon
            elif pot['success'] == False:
                return print(f"Vous avez déjà ouvert votre pot aujourd'hui, il vous a rapporté {user.stats_today()['winning']['credits']} credits !")

    except:
        return print("Erreur lors de la connexion")


email = "exemple@exemple.com"
mdp = "1234"

pot_honeygain(email, mdp)
