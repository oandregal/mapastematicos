# Parser for CSV INE files (abredatos.org)

#import csv
import getopt
import sys, os

def usage():
    print('Usage: python *.py -f file.csv')
    print('Wrong argument')

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "f:", ["help","ayuda"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-f':
            csvfile = arg
        else:
            usage()
            exit()
    execute(csvfile)


def cleanString(s):
    """Clean strings for spaces, final dots, strange numbers, etc...."""
    #### TODO

    # Remove  dots at the end of the string
    while s[-1]=='.':
        s = s[0:-1]

    # Remove '(' and ')' sections
    while s.find('(')!=-1:
        start = s.find('(')
        end = s.find(')', start)+1
        if end > start:
            s = s[0:start]+s[end:]

    # Remove spaces
    s = s.strip()

    # Remove doubles spaces
    while s.find('  ')!=-1:
        s = s.replace('  ', ' ')

    return s;


def checkIfINE(csvfile):
    """ Detects if the file is a CSV file on the INE format"""
    #TODO
    return True;

def getDataSource(csvfile):
    """Get DataSource"""

    reader = open(csvfile, "rb")
    for line in reader:
        if line.find('Fuente:') != -1:
            start = line.find(':') +1 
            aux = cleanString(line[start:])
            print '------> SOURCE: ' + aux
            return aux
    

def getUnits(csvfile):
    """Get Units of the report"""

    # TODO It is always at the row 5
    reader = open(csvfile, "rb")
    for line in reader:
        if line.find('Unidades:') != -1:
            start = line.find(':') +1 
            aux = cleanString(line[start:])
            print '-----> UNITS: ' + aux
            return aux


def getTitle(csvfile):
    """Get Title of the report"""
    reader = open(csvfile, "rb")
    ## Skip first lines that have Categories
    n_row = 0
    for line in reader:
        n_row = n_row +1
        # TODO It is always at the row 3
        if n_row == 4:
            aux = cleanString(line)
            print '--> TITLE: ' + aux
            return aux


def getNotes(csvfile):
    """Get Notes of the report if they exist"""

    ## Skip first lines that have Categories
    reader = open(csvfile, "rb")
    n_row = 0
    notesText = ''
    notesSection = False
    for line in reader:
        # TODO It is always at the row 3
        n_row = n_row +1
        if line.find('Fuente:') != -1:
            notesSection = False
            return notesText

        if notesSection:
            aux = cleanString(line)
            ######### Cleaning
            if (len(aux)>1):
                # Sometimes it is needed that process:
                aux = aux.replace('NOTA', '')
                aux = aux.replace('NOTA:', '')
                aux = aux.replace('Nota:', '')
                if (aux.startswith('1.-')):
                    aux = aux[4:]
                if (aux.startswith('1.- ')):
                    aux = aux[4:]
                if (aux.startswith('1 .-')):
                    aux = aux[5:]
                if (aux[1] == ')'):
                    aux = aux[2:]
                aux = cleanString(aux)
                ####################
                notesText = notesText + aux + '\n'
                print '------> NOTE: ' + aux

        if line.find('Notas:') != -1:
            notesSection = True

    return notesText

def getCopyright(csvfile):
    """Get Copyrigth of the report"""

    # TODO It is always at the row 5
    reader = open(csvfile, "rb")
    for line in reader:
        if line.lower().find('copyright') != -1:
            start = line.find('ght') +4 
            aux = cleanString(line[start:])
            print '----------> COPY: ' + aux
            return aux

def getTags(csvfile):
    """Get Tags of the report looking Categories"""

    # TODO It is always at the row 1 and 2
    reader = open(csvfile, "rb")
    n_row = 0
    tags = list()
    for line in reader:
        n_row = n_row +1
        if n_row < 2:
            aux = cleanString(line)
            tags = identifyTags(aux)
            print '--> TAG: ' + aux
        else: 
            break
    return aux        

def identiftyTags(s):
    


def execute(csvfile):

    checkIfINE(csvfile)

    reader = open(csvfile, "rb")
    #TODO Check if delimitir is ';'
    # reader = csv.reader(open(csvfile, "rb"), delimiter=';')
    # csvheader = reader.next()

    getTitle(csvfile)
    getUnits(csvfile)
    getNotes(csvfile)
    getDataSource(csvfile)
    getCopyright(csvfile)
    getTags(csvfile)




if __name__ == "__main__":
    main(sys.argv[1:])
