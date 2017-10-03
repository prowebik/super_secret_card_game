import cards
import network
import time

class Player:
    def __init__(self):
        self.cards = []
        self.coins = 10000
        self.id = None
        self.server = None
        self.s = None
        self.main()
        self.playing=False
        self.letstart=None

    def send(self, msg):
        if self.s is None:
            self.s = network.Client()
        self.s.send(msg)

    def recv(self):
        if self.s is None:
            self.s = network.Client()
        return self.s.recv()

    def wait(self):
        print('Ожидание карт')
        for i in range(2):
            self.cards.append(self.recv())
            print('Получена карта', self.cards[-1])

    def round(self):
        message = self.recv()
        while 'ask' in message or 'info' in message:
            if 'info' in message:
                print(message)
            if 'ask' in message:
                while True:
                    ans = input('сделайте ваш ход (pass(p)/call(c)/rise(r)): ')
                    if ans == 'p':
                        self.send('pass')
                        break
                    elif ans == 'c':
                        self.send('call')
                        break
                    elif ans == 'r':
                        self.send('rise')
                        break
                    else:
                        print('я вас не понимаю')
            message = self.recv()
        print(message)

    def game(self):
        for i in range(4):
            self.round()

    def main(self):
        if input('Подключиться к серверу (yes(y)/no(n))?: ').lower() == 'y':
            print(self.recv())#Логин
            self.send(input())
            self.playing=True
            print(self.recv())#Добро пожаловать
            money = self.recv()
            self.send("All is norm")
            print('Ваши деньги:' + money + "\n")
            print("Регистрация на сервере успешно выполнена.")
            self.id = self.recv()
            time.sleep(0.1)
            while self.playing:
                self.letstart=self.recv()
                self.wait()
                self.game()
            #print('Ваши деньги:' + money + "\n")
        else:
            print('By!')
            exit(0)

player = Player()
