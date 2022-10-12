# Importations
from pyHoneygain import HoneyGain, HoneygainAPIError
import telebot
import time
import schedule
from threading import Thread



API_KEY = # Votre clef api (str)
CHAT_ID = # Votre chat id (int)
bot = telebot.TeleBot(API_KEY)



def pot_honeygain(email:str, mdp:str):
    try:
        
        user = HoneyGain()
        user.login(email, mdp)
        pot = user.open_honeypot()
        if pot['success'] == True:
            bot.send_message(chat_id=CHAT_ID, text=f"Vous venez de gagner {str(pot)[0:-2]} credits !")
        elif pot['success'] == False:
            message_envoye = bot.send_message(chat_id=CHAT_ID, text=f"Vous avez déjà ouvert votre pot aujourd'hui.\nIl vous a rapporté {str(user.stats_today()['winning']['credits'])[0:-2]} credits !\nCe message va s'autodétruire dans 30 secondes")
            time.sleep(30)
            bot.delete_message(chat_id=CHAT_ID, message_id=message_envoye.message_id)
        return 'Execution terminée'


    except telebot.apihelper.ApiException:
        return 'Erreur avec Telebot'
    
    except HoneygainAPIError:
        erreur_msg = bot.send_message(chat_id=CHAT_ID, text="Erreur lors de la connexion à Honeygain")
        time.sleep(10)
        bot.delete_message(chat_id=CHAT_ID, message_id=erreur_msg.message_id)
        return 'Erreur avec Honeygain'
    



email = "exemple@gmail.com"
mdp = "1234"


print('Execution en cours...')


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)
def daily():
    print(pot_honeygain(email, mdp))
    


schedule.every().day.at("04:30").do(daily)

Thread(target=schedule_checker).start() 



@bot.message_handler(commands=['isactive'])
def is_active(message):
    is_active_msg = bot.reply_to(message, text="Yes")
    time.sleep(3)
    bot.delete_message(chat_id=CHAT_ID, message_id=is_active_msg.message_id)
    bot.delete_message(chat_id=CHAT_ID, message_id=message.message_id)
    


@bot.message_handler(commands=['pot'])
def command_pot(message):
    bot.delete_message(chat_id=CHAT_ID, message_id=message.message_id)
    print(pot_honeygain(email, mdp))
    

'''
@bot.message_handler(commands=['stop'])
def stop(message):
    bot.delete_message(chat_id=CHAT_ID, message_id=message.message_id)
    bot.stop_polling()
    print('oui')
'''
    
bot.send_message(chat_id=CHAT_ID, text="Commandes disponibles:")
bot.send_message(chat_id=CHAT_ID, text="isactive : Vérifie si le bot est actif\npot : Ouvre le pot")

bot.polling()



    
        

