from random import randint


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1 for i in range(self._length)]

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):

        if self._is_move == True:
            if self._tp == go:
                self._x +=go
            else:
                self._y +=go


    def is_collide(self, ship):

        if self._tp == 1:
            res = [[(self._x + j, self._y + i) for j in range(-1, self._length+1)] for i in range(-1, 2)]

        else:
            res = [[(self._x + i, self._y + j) for j in range(-1, self._length+1)] for i in range(-1, 2)]

        if ship._tp == 1:
            other = [(ship._x + i, ship._y) for i in range(ship._length)]
        else:
            other = [(ship._x, ship._y + i) for i in range(ship._length)]
        coords = []
        for i in range(len(res)):
            coords.extend(res[i])
        return not all([i not in coords for i in other])

    def is_out_pole(self, size):
        if self._tp == 1:
            total = [(self._x + i, self._y) for i in range(self._length)]
        else:
            total = [(self._x, self._y + i) for i in range(self._length)]

        return not all([ 0<=i<size and 0<=j<size for i,j in total])

    def get_coords(self):
        if self._tp == 1:
            total = [(self._x + i, self._y) for i in range(self._length)]
        else:
            total = [(self._x, self._y + i) for i in range(self._length)]
        return total

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self.init()

    def init(self):
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2))]

        c=0
        while c!=10:

            c=0
            for i in self._ships:
                res = False
                k = 0
                if k == 100:
                    break
                while not res:
                    k+=1
                    if k == 100:
                        break
                    x, y = randint(0,self._size-1), randint(0, self._size - 1)
                    i._x = x
                    i._y = y
                    if i.is_out_pole(self._size):
                        continue
                    for j in self._ships:
                        if i == j or j._x == None:
                            continue
                        if i.is_collide(j):
                            break
                    else:
                        res = True
                        c+=1
            if c!= 10:
                for l in self._ships:
                    l._x = None
                    l._y = None

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for i in self._ships:
            tmp = (i._x, i._y)
            if i._tp==1:
                i._x +=1
            else:
                i._y +=1

            for j in self._ships:

                if i == j:
                    continue
                if i.is_collide(j) or i.is_out_pole(self._size):
                    i._x, i._y = tmp
                    break
            else:
                continue

            if i._tp == 1:
                i._x -= 1
            else:
                i._y -= 1

            for j in self._ships:
                if i == j:
                    continue
                if i.is_collide(j) or i.is_out_pole(self._size):
                    i._x, i._y = tmp
                    break

    def show(self):
        res = [[0 for i in range(self._size)] for j in range(self._size)]

        for i in self._ships:
            tmp = i.get_coords()

            for j, r in zip(tmp, i._cells):
                res[j[0]][j[1]] = r
        print('   ', end='')
        for i in range(self._size):
            print(str(i).ljust(3), end='')
        print()

        for n,i in enumerate(res):
            print(str(n).ljust(3), end='')
            for j in i:
                print(str(j).ljust(3), end = '')
            print()

    def get_pole(self):
        res = tuple([[0 for i in range(self._size)] for j in range(self._size)])
        for i in self._ships:
            tmp = i.get_coords()

            for j, r in zip(tmp, i._cells):
                res[j[0]][j[1]] = r
        for i in res:
            i[:] = tuple(i)

        return res



class StartGame:

    def __init__(self, size):
        self.computer = GamePole(size)
        self.user = GamePole(size)
        self.size = size
        self.computer_steps=[]
        self.user_steps = []




    def check_fly(self, x, y, pole='computer'):
        ships = self.computer.get_ships() if pole == 'computer' else self.user.get_ships()
        for i in ships:
            coords = i.get_coords()

            if (x,y) in coords:
                if all([j == 3 for j in i._cells]):
                    return "Корабль уже уничтожен"

                i[coords.index((x,y))]=2
                who = 'Игрок' if pole == 'computer' else 'Компьютер'
                if all([j == 2 for j in i._cells]):
                    i._cells[:] = [3 for j in range(len(i._cells))]
                    res = self.check_winner(who)
                    if res:
                        return res
                    return "Попал, корабль уничтожен"
                return "Попал"
        return 'Мимо'

    @staticmethod
    def get_list_coords(pole: list, size: int, x: int, y: int):
        coords = [(x, y)]
        for i in range(1, 4):
            if 0 <= x - i < size:
                if pole[x - i][y] != 0:
                    coords.append((x - i, y))
                else:
                    break

        for i in range(1, 4):
            if 0 <= x + i < size:
                if pole[x + i][y] != 0:
                    coords.append((x + i, y))
                else:
                    break

        for i in range(1, 4):
            if 0 <= y - i < size:
                if pole[x][y-i] != 0:
                    coords.append((x, y-i))
                else:
                    break

        for i in range(1, 4):
            if 0 <= y + i < size:
                if pole[x][y+i] != 0:
                    coords.append((x, y+i))
                else:
                    break
        return coords


    def check_fly_list(self, pole: list, size: int, x: int, y: int, my = False):
        if pole[x][y] not in (0,4):
            coords = self.get_list_coords(pole, size, x, y)
            if pole[x][y] == 3 or pole[x][y] == 2:
                if all(pole[x1][y1]==3 for x1,y1 in coords):
                    return 'Корабль уже уничтожен', pole
                else:
                    return 'Вы уже попали в этот корабль', pole
            else:
                pole[x][y] = 2
                if all(pole[x1][y1]==2 for x1,y1 in coords):
                    for x1,y1 in coords:
                        pole[x1][y1]=3
                    if my:
                        self.pole = pole
                    res = self.check_winner_list(pole)
                    if res:
                        return res, pole
                    return "Попал, корабль уничтожен", pole
                if my:
                    self.pole = pole
                return "Попал", pole
        pole[x][y] = 4
        return 'Мимо', pole

    @staticmethod
    def check_winner_list(pole):
        res = '😁 Поздравляем, вы выиграли!💪'
        for i in pole:
            for j in i:
                if j in (1,2):
                    return False
        return res



    def check_winner(self, who):
        ships = self.computer.get_ships() if who == 'Игрок' else self.user.get_ships()
        if all([all([j == 3 for j in i._cells]) for i in ships]):

            return 'Вы выиграли! Поздравляем!' if who == 'Игрок' else 'Вы проиграли.'
        return False

    def computer_step(self):

        x,y = randint(0,self.size-1),randint(0,self.size-1)
        while (x,y) in self.computer_steps:
            x, y = randint(0, self.size - 1), randint(0, self.size - 1)
        self.computer_steps.append((x,y))
        return x,y








SIZE_GAME_POLE = 8

'''pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()

pole.move_ships()
print()
pole.show()
print(pole.get_pole())'''
def go_play(SIZE_GAME_POLE):
    game=StartGame(SIZE_GAME_POLE)
    print("Игра \"Морской бой\"")
    while True:
        a = input('Ваш ход: ').split()
        if len(a) == 2 and a[0].isdigit() and a[1].isdigit() and 0 <= int(a[0]) < SIZE_GAME_POLE and 0 <= int(
                a[1]) < SIZE_GAME_POLE:

            res = game.check_fly(int(a[0]), int(a[1]))
            print(res)
            if 'выиграл' in res:
                break
        else:
            continue
        x, y = game.computer_step()
        res = game.check_fly(x, y, 'Игрок')
        print(f'Ход компьютера: {x} {y}')
        print(res)
        if 'выиграл' in res:
            break

        game.computer.show()
        print()
        game.user.show()










