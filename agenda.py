import csv


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Contacto:
    def __init__(self, name, lastname, number):
        self.name = name
        self.lastname = lastname
        self.number = number

    def getInfo(self):
        return [self.name, self.lastname, self.number]

    def getName(self):
        return self.name

    def getLastname(self):
        return self.lastname

    def getFullName(self):
        return self.name + ' ' + self.lastname

    def getNumber(self):
        return self.number


class Agenda:
    def __init__(self, filePath):
        self.contactList = []
        self.filePath = filePath
        # self.file = open(filePath, 'r+')
        self.header = []
        self.importFromCSV()

    def añadirContacto(self):
        localFile = open(self.filePath, 'a')
        writer = csv.writer(localFile)
        name = input('\nenter name:\n')
        lastname = input('\nenter lastname:\n')
        number = input('\nenter phone number:\n')
        newContact = Contacto(name, lastname, number)

        # se añade el contacto a la clase agenda y al csv al mismo tiempo
        self.contactList.append(newContact.getInfo())
        writer.writerow(newContact.getInfo())
        print(bcolors.OKGREEN + '\ncontacto guardado:',
              str(newContact.getInfo()))

    def importFromCSV(self):
        print('importando contactos...')
        localFile = open(self.filePath, newline='')
        reader = csv.reader(localFile)
        fileHeader = next(reader)
        fileContent = [row for row in reader]
        # gardar cabecera
        self.header = fileHeader
        # para cada linea de csv crear un contacto e introducirlo en la clase agenda
        for row in fileContent:
            newContact = Contacto(row[0], row[1], row[2])
            self.contactList.append(newContact)
        print(bcolors.OKGREEN + 'se han importando ' +
              str(len(fileContent)) + ' contactos\n' + bcolors.ENDC)

    def buscarContacto(self):
        inputFilter = input('introduce el campo de busqueda\n')
        filterField = ''
        columnIndex = False
        for col in self.header:
            if col == inputFilter:
                filterField = col
                columnIndex = self.header.index(col)

        if (filterField != ''):
            filterValue = input('introduce el ' + filterField + ' a buscar\n')
            foundContacts = self.getContactsByColumn(columnIndex, filterValue)
            numOfFoundContacts = len(foundContacts)
            if foundContacts:
                print('ha habido ' + str(numOfFoundContacts) + ' coincidencia/s: ')
                print(foundContacts)
            else:
                print('no hay ninguna coincidencia')
        else:
            print(bcolors.FAIL + 'el campo que buscas no existe')

    def getContactsByColumn(self, columnIndex, filter):
        coincidences = []
        for contact in self.contactList:
            currentContactData = contact.getInfo()
            fieldToSearch = currentContactData[columnIndex]

            if(fieldToSearch == str(filter)):
                coincidences.append(currentContactData)

        return coincidences

    def getTableHeader(self):
        return self.header

    def imprimirContactos(self, printMode):
        tableHeader = str(self.getTableHeader())
        printed = 0
        for contact in self.contactList:
            if (printMode == 'no'):
                if printed == 0:
                    print('\n' + bcolors.OKBLUE + tableHeader + bcolors.ENDC)
                    printed = 1
                print(contact.getInfo())
            elif printMode == 'nombre':
                print(contact.getName())
            elif printMode == 'apellido':
                print(contact.getLastname())
            elif printMode == 'nombre completo':
                print(contact.getFullName())
            elif printMode == 'numero':
                print(contact.getNumber())


# inicializar agenda al arrancar la aplicacion
agenda = Agenda('./agenda.csv')


# preguntar el modo de ejecucion
print('Bienvenido a tu agenda!\n')
mode = input('¿Quieres "añadir" o "buscar" un contacto?\n')
if (mode == 'añadir'):
    agenda.añadirContacto()
elif (mode == 'buscar'):
    agenda.buscarContacto()
elif (mode == 'list'):
    printMode = input('¿quieres añadir un filtro?')
    agenda.imprimirContactos(printMode)
