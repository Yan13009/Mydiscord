import socket
import threading

# Définir l'hôte et le port pour correspondre à ceux du serveur
host = '10.10.77.63'
port = 50000

# Créer le socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se connecter au serveur
client.connect((host, port))

# Recevoir le message du serveur et décoder
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                # Envoyer le nickname au serveur
                client.send(nickname.encode('ascii'))
            elif message == 'PASS':
                # Envoyer le mot de passe si nécessaire
                client.send(password.encode('ascii'))
            elif message == 'REFUSE':
                print("Connexion refusée par le serveur.")
                break
            elif message == 'BAN':
                print("Vous avez été banni par l'administrateur.")
                break
            else:
                print(message)
        except:
            # Fermer la connexion en cas d'erreur
            print("Une erreur est survenue!")
            client.close()
            break

# Envoyer des messages au serveur
def write_message():
    while True:
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+7:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+6:]}'.encode('ascii'))
        else:
            client.send(message.encode('ascii'))

# Demander le nickname
nickname = input("Choisissez votre pseudo: ")
if nickname == 'admin':
    password = input("Entrez le mot de passe administrateur: ")

# Démarrer le thread pour écouter les messages du serveur
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Démarrer le thread pour écrire des messages
write_thread = threading.Thread(target=write_message)
write_thread.start()