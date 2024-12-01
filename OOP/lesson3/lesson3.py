


class Person :
    def __init__(self,name:str,surname:str,skill=1):
        self.name = name
        self.surname = surname
        self.skill = skill

    def __del__(self):
        print('До свидания мистер',self.name,self.surname)

    def info (self):
        return '{} {},{}'.format(self.name,self.surname,self.skill)
    pass

worker = Person("И","Котов",2)
helper = Person('О','Пидор',"1488")
maker = Person('Чмо','Идиот',"Мудак")

print(helper.info())
print(maker.info())
del helper
print("Конец программы")
input()