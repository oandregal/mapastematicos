#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 mapastematicos.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Software developed for abredatos 2010
#
# AUTHORS:
# Francisco Puga Alonso <fran.puga@gmail.com> <http://conocimientoabierto.es>
# Andres Maneiro Boga <andres.maneiro@gmail.com> <http://nosolosoftware.es>
# Adrián Eiris
# Nacho Varela

## Parser for CSV INE files (abredatos.org)

import getopt
import sys, os, codecs

PROV_DICT_FILE = 'dict_provincias.csv'
CCAA_DICT_FILE = 'dict_ccaa.csv'
TAG_DICT_FILE = 'dict_tags.csv'

# Dictionary of NAME and string identifiers for CCAA and provinces
provDict = None
ccaaDict = None

# Dictionary of TAGS and string identifiers of them
tagDict = None


def usage():
    print('Usage: python *.py -f file.csv')
    print('Wrong argument')
    print('IMPORTANT: On the same directory of this script should be placed 3 CSV files of dictionaries:  "dict_provincias.csv", "dict_ccaa.csv" and "dict_tags.csv"')

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

def cleanEncodingLower(s):
    s  =  cleanString(s).lower()
    s = s.replace('á', 'a')
    s = s.replace('é', 'e')
    s = s.replace('í', 'i')
    s = s.replace('ó', 'o')
    s = s.replace('ú', 'u')
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
                    h = header[i] + '-' + cleanColumns(getPreviousNotNullString(aux, i))
                    #print "h: " + header[i] + " aux: " + cleanColumns(getPreviousNotNullString(aux, i))
                    header[i] = h
            #### TODO If there is a year on the Column put as first String????????????
            print str(n_row) + str(header)
        if not isHeaderSection:
            break
    return header


def getCCAADictionary():
    """" Opens a file with CCAA and identifiers and  creates a dict"""

    global ccaaDict
    global CCAA_DICT_FILE

    if ccaaDict != None:
        return ccaaDict
    else:
        ccaaDict = dict()
        print(CCAA_DICT_FILE)
        dict_r = open(CCAA_DICT_FILE, 'rb')
        for line in dict_r:
            line = line.replace('"', '')
            aux = line.split(';')
            name = ''
            if len(aux)>0:
                name = cleanString(aux[0])
                for s in aux[1:]:
                    ##### OJO CON ENCODING
                    s  =  cleanEncodingLower(s)
                    if len(s)>0:
                        ccaaDict[s] = name
            else:
                pass

#    print("\n\n")
#    print(provDict)
#    print("\n\n")
    return ccaaDict

def getProvDictionary():
    """" Opens a file with Provinces and identifiers and  creates a dict"""

    global provDict
    global PROV_DICT_FILE

    if provDict != None:
        return provDict
    else:
        provDict = dict()
        print(PROV_DICT_FILE)
        dict_r = open(PROV_DICT_FILE, 'rb')
        for line in dict_r:
            line = line.replace('"', '')
            aux = line.split(';')
            name = ''
            if len(aux)>0:
                name = cleanString(aux[0])
                for s in aux[1:]:
                    ##### OJO CON ENCODING
                    s = cleanEncodingLower(s)
                    if len(s)>0:
                        provDict[s] = name
            else:
                pass

#    print("\n\n")
#    print(provDict)
#    print("\n\n")
    return provDict


def getCorrectProvName(s):

    s = cleanString(s).lower() 

    provDict  =  getProvDictionary()
    for k in provDict.keys():
        #print s + '  ' +  k + '  ' + str(s.find(k))
        if s.find(k) != -1:
            return provDict.get(k)
    return None


def getCorrectCCAAName(s):

    s = cleanString(s).lower() 

    ccaaDict  =  getCCAADictionary()
    for k in ccaaDict.keys():
        #print s + '  ' +  k + '  ' + str(s.find(k))
        if s.find(k) != -1:
            return ccaaDict.get(k)
    return None


###################################################### TODO
###################################################### TODO
###################################################### TODO make the dict CCAAA!!!!

def getReportData(csvfile):
    """Get report data of the table."""

    # TODO It is always starts at 9
    reader = open(csvfile, "rb")
    n_row = 0
    dataProv = list()
    dataCCAA = list()
    isDataSection = False

    for line in reader:
        n_row = n_row +1

        line = cleanString(line)
        if n_row >= 8 and not isDataSection:
            #print 'HEADER' + str(n_row)

            #When there is text  in the first column  data section starts 
            if line[0]!=';':
                isDataSection = True

        if n_row >= 8 and isDataSection:
#            print 'DATA' + str(n_row) + '   ' + line
            line = cleanString(line)

            if len(line) == 0:
                break
            
            row = line.split(';')
            rowName = getCorrectProvName(row[0])
            if rowName != None:
                print "Encontre un PROV: " + rowName
                row[0] = rowName
                dataProv.append(row)
            else:
                print "Row ["+row[0]+"] is NOT a  Province"

            rowName = getCorrectCCAAName(row[0])
            if rowName != None:
                print "Encontre un CCAA: " + rowName
                row[0] = rowName
                dataCCAA.append(row)
            else:
                print "Row ["+row[0]+"] is NOT a  CCAA"

    ## Choose one of the 2 data 
    if (len(dataCCAA)>=len(dataProv)):
        data = dataCCAA
    else:
        data = dataProv

    print data
    return data

#########################################################################################


def identifyTags(s):
    ##### TODO
    ## It takes a dictionary of tags defined on a csv (tag;autotag;synonym1;..;synonymN)
    tags = list()
    return tags


def execute(csvfile):

    checkIfINE(csvfile)

    reader = open(csvfile, "rb")

    title = getTitle(csvfile)
    units = getUnits(csvfile)
    notes = getNotes(csvfile)
    source = getDataSource(csvfile)
    copy = getCopyright(csvfile)
    columns = getReportColumns(csvfile)
    data = getReportData(csvfile)
    tags = getTags(csvfile)

if __name__ == "__main__":
    main(sys.argv[1:])
