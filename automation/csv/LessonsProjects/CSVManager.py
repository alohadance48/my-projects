import csv

def main():
    class ReadCSVDocument:
        def __init__(self):
            self.filepath = None
            self.content = None


        def setFilepath(self):
            self.filepath = input("Enter file path: ")


        def readFile(self):
            with open(self.filepath,'r',encoding='utf-8') as file:
                self.content = file.readlines()

        def writeFileCSV(self):
            with open('output.csv','w',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Line'])

                for line in self.content:
                    writer.writerow([line.strip()])



if __name__ == '__main__':
    main()