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
    if len(s)==0:
        return ''

    # Remove  dots at the end of the string
    while s[-1]=='.':
        s = s[0:-1]

    # Remove '(' and ')' sections
    while s.find('(')!=-1:
        start = s.find('(')
        end = s.find(')', start)+1
        if end > start:
            s = s[0:start]+s[end:]

    # Remove '-' and '_' chars
    s = s.replace('-', '')
    s = s.replace('_', '')

    # Remove initial and final spaces 
    s = s.strip()

    # Remove doubles spaces
    while s.find('  ')!=-1:
        s = s.replace('  ', ' ')

    return s;


def cleanColumns(s):
    s = cleanString(s)
    s = s.replace(' ', '_')
    return s


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
    isNotesSection = False
    for line in reader:
        # TODO It is always at the row 3
        n_row = n_row +1
        if line.find('Fuente:') != -1:
            isNotesSection = False
            return notesText

        if isNotesSection:
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
            isNotesSection = True

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
    ## TODO FIELD????????????????????????????????
    for line in reader:
        n_row = n_row +1
        if n_row < 5:
            aux = cleanString(line)
            tags = identifyTags(aux)
            print '--> TAG: ' + aux
        else: 
            break
    return aux






########################################################################################
## DATA

def getPreviousNotNullString(l, start_idx):
    """Gets the previous string from before 'start_idx' index that is not null"""
    aux = ''
    for s in l[0:start_idx+1]:
        if len(s)>0:
            aux = s
    return aux

def getRowDictionary():
    """" Opens a file with CCAA and Provinces and """
    ### TODO
    pass

# def getReportColumns(csvfile):
#     """Get report columns of the table. When complex columns (more than one level) create a simple one merging them.
#            Spaces on the columnames are changed for '_' chars. Multiple level columns are separated by '-' char."""

#     rowDict =  getRowDictionary()

#     # TODO It is always starts at 9
#     reader = open(csvfile, "rb")
#     n_row = 0
#     header = list()
#     isHeaderSection = True

#     for line in reader:
#         n_row = n_row +1
        
#         if n_row >= 8 and isHeaderSection:
#             line = cleanString(line)
#             ## When there is text  in the first column  data section starts 
#             if line[0]!=';':
#                 isHeaderSection = False
#                 break
#             if len(header)==0:
#                 header = line.split(';')
#                 for i in range(0, len(header)):
#                     h = cleanColumns(header[i])
#                     if len(h)==0:
#                         h = getPreviousNotNullString(header, i)
#                     header[i] = h
#             else:
#                 aux = line.split(';')
#                 for i in range(0, len(header)):
# #                    print str(n_row) +"--" + str(i)
#                     #print 'HEADER: ' + str(header)
#                     #print 'LINE: ' + str(aux)
#                     #print 'PREVIOUS: ' + h
# #                    if len(header[i])>1:
# #                    print "h: " + header[i] + " aux: " + cleanColumns(getPreviousNotNullString(aux, i))
#                     h  = header[i] + '-' + cleanColumns(getPreviousNotNullString(aux, i))
#                     if (len(cleanColumns(h)) >0):
#                         header[i] = header[i] + '-' + cleanColumns(getPreviousNotNullString(aux, i))

#                     #h_aux.append(aux2)
#                         #print 'NEW: ' + aux2
#             #### TODO If there is a year on the Column put as first String????????????
#             print str(n_row) + str(header)

#         return header
#         if not isHeaderSection:
#             break                
#     return n_row


def getReportColumns(csvfile):
    """Get report columns of the table. When complex columns (more than one level) create a simple one merging them.
           Spaces on the columnames are changed for '_' chars. Multiple level columns are separated by '-' char."""

    # TODO It is always starts at 9
    reader = open(csvfile, "rb")
    n_row = 0
    header = list()
    isHeaderSection = True

    for line in reader:
        n_row = n_row +1
        
        if n_row >= 8 and isHeaderSection:
            line = cleanString(line)
            ## When there is text  in the first column  data section starts 
            if line[0]!=';':
                isHeaderSection = False
                break
            if len(header)==0:
                header = line.split(';')
                for i in range(0, len(header)):
                    h = cleanColumns(header[i])
                    if len(h)==0:
                        h = getPreviousNotNullString(header, i)
                    header[i] = h
            else:
                aux = line.split(';')
                h_aux = list()
                for i in range(0, len(header)):
                    #print str(n_row) +"--" + str(i)
                    #print 'HEADER: ' + str(header)
                    #print 'LINE: ' + str(aux)
                    #print 'PREVIOUS: ' + h
                    h = header[i] + '-' + cleanColumns(getPreviousNotNullString(aux, i))
#                    if len(h.replace('-',''))>0:
                        #print "h: " + header[i] + " aux: " + cleanColumns(getPreviousNotNullString(aux, i))
                    header[i] = h
                    #h_aux.append(aux2)
                        #print 'NEW: ' + aux2
            #### TODO If there is a year on the Column put as first String????????????
            print str(n_row) + str(header)
        if not isHeaderSection:
            break
    return header



def getReportData(csvfile):
    """Get report data of the table."""

    rowDict =  getRowDictionary()

    # TODO It is always starts at 9
    reader = open(csvfile, "rb")
    n_row = 0
    header = list()
    isHeaderSection = True

    for line in reader:
        n_row = n_row +1
        
        if n_row >= 8 and isHeaderSection:
            line = cleanString(line)
            ## When there is text  in the first column  data section starts 
            if line[0]!=';':
                isHeaderSection = False
                break
            if len(header)==0:
                header = line.split(';')
                for i in range(0, len(header)):
                    h = cleanColumns(header[i])
                    if len(h)==0:
                        h = getPreviousNotNullString(header, i)
                    header[i] = h
            else:
                aux = line.split(';')
                h_aux = list()
                for i in range(0, len(header)):
#                    print str(n_row) +"--" + str(i)
                    #print 'HEADER: ' + str(header)
                    #print 'LINE: ' + str(aux)
                    #print 'PREVIOUS: ' + h
#                    if len(h)>0:
#                    print "h: " + header[i] + " aux: " + cleanColumns(getPreviousNotNullString(aux, i))
                    header[i] = header[i] + '-' + cleanColumns(getPreviousNotNullString(aux, i))
                    #h_aux.append(aux2)
                        #print 'NEW: ' + aux2
            #### TODO If there is a year on the Column put as first String????????????
            print str(n_row) + str(header)
        if not isHeaderSection:
            break
    return header


#########################################################################################
def identifyTags(s):
    ##### TODO
    ## It takes a dictionary of tags defined on a csv (tag;autotag;synonym1;..;synonymN)
    tags = list()
    return tags


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
    getReportColumns(csvfile)
#    getReportData(csvfile)
    getTags(csvfile)


if __name__ == "__main__":
    main(sys.argv[1:])
