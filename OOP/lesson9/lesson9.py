from math import pi


def main():
    class Culinder :
        @staticmethod
        def make_area(d,h):
            circle = pi * d ** 2/4
            side = pi * d * h
            return  round(circle*2 + side , 2)
        def __init__(self,dia,h):
            self.__dict__['dia'] = dia
            self.__dict__['h'] = h
            self.__dict__['area']= self.make_area(dia,h)
            pass
        def __setattr__(self, key, value):
            if key == 'dia':
                self.__dict__['dia' ] = value
                self.__dict__['area']  = self.make_area(self.__dict__['area'],self.__dict__['h'])
            elif key == 'h':
                self.__dict__['h'] = value
                self.__dict__['area'] = self.make_area(self.__dict__['dia'],self.__dict__['h'])
            elif key == 'area':
                print('хуй')
            pass


    a = Culinder(1, 2 )
    print(a.area)
    print(a.make_area(2,2))
    pass

if __name__ == '__main__':
    main()