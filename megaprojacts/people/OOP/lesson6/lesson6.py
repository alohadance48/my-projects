def main():
    class Test :
        def __init__(self,test):
            self.test = test
            pass
        def new_number (test:bool):
            return test
        def main_number (self,test):
            if isinstance(test,(float,int)):
                self.test = test
            else :
                raise ValueError('Тупой')
            pass
    obj = Test(20)
    print(obj.new_number())
    obj.main_number(20)
    print(obj.new_number())
    try:
        obj.main_number('Heloo')
    except ValueError as e :
        print(e)


    pass

if __name__ == '__main__':
    main()