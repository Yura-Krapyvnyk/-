import socket, threading, time

alphabet = "abcdefghijklmnopqrstuvwxyzaабвгдеєжзиійклмнопрстуфхцчшщьюяа12345678901"

shutdown = False
join = False


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)

                decrypt = ""
                k = False
                for i in data.decode("utf-8"):
                    if i == ":":
                        k = True
                        decrypt += i
                    elif k == False or i == " ":
                        decrypt += i
                    else:
                        decrypt += chr(ord(i) + 0)
                print(decrypt)

                time.sleep(0.2)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0

server = (" 192.168.0.173", 4040)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = input("Ім'я: ")

print("\nВи ввели ім'я! \n ")
print(alias + " вітаємо вас в чаті Цезаря!")

choise = ""
choise_variant = ["+", "-", "="]

while choise not in choise_variant:
    choise = input('''
Щоб приймати зашифровані повідомлення введіть (+)

Щоб приймати розшифровані повідомлення введіть (-)

Щоб приймати повідомлення без шифру (=)

Вибір: ''')

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

while shutdown == False:
    if join == False:
        s.sendto(("[" + alias + "] => приєднався до чату ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()
            message = message.lower()
            key = 1
            crypt = ""

            if choise == "+":
                for letter in message:
                    position = alphabet.find(letter)
                    newposition = position + key
                    if letter in alphabet:
                        crypt = crypt + alphabet[newposition]
                    else:
                        crypt = crypt + letter

            elif choise == "-":
                for letter in message:
                    position = alphabet.find(letter)
                    newposition = position - key
                    if letter in alphabet:
                        crypt = crypt + alphabet[newposition]
                    else:
                        crypt = crypt + letter
            elif choise == "=":
                for letter in message:
                    position = alphabet.find(letter)
                    newposition = position - 0
                    if letter in alphabet:
                        crypt = crypt + alphabet[newposition]
                    else:
                        crypt = crypt + letter

            message = crypt

            if message != "":
                s.sendto(("[" + alias + "] :: " + message).encode("utf-8"), server)

            time.sleep(0.2)
        except:
            s.sendto(("[" + alias + "] <= вийшов з чату ").encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()

import socket, time

host = socket.gethostbyname(socket.gethostname())
port = 4040

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

quit = False
print("[ Сервер працює ]")

while not quit:
    try:
        data, addr = s.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)

        itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

        print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + itsatime + "]/", end="")
        print(data.decode("utf-8"))

        for client in clients:
            if addr != client:
                s.sendto(data, client)
    except:
        print("\n[ Сервер зупинився ]")
        quit = True

s.close()
