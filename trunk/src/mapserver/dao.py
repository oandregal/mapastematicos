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
# Adrián Eiris Torres <adrianet82@gmail.com> <http://jauladepalabras.netii.net/>
# Nacho Varela  García <nachouve@gmail.com> <http://libresig.blogspot.com/>


import psycopg2

class DAOClass:
    
    # RGB de los 5 rangos que vamos a emplear
    # No debería ir aquí pero resulta cómodo porque vamos a compartir esta clase

    # color0 = '204 255 204'
    color0H = 'ccffcc'
    # color1 = '164 204 184'
    color1H = 'a4ccb8'
    # color2 = '124 153 164'
    color2H = '7c99a4'
    # color3 = '84 102 144'
    color3H = '546690'
    # color4 = '44 51 124'
    color4H = '2c337c'

    color = ['204 255 204', '164 204 184', '124 153 164', '84 102 144', '44 51 124']
    
    
    def __init__(self):
        # self.conn = psycopg2.connect(self.getConnectionString())
        # self.cur = self.conn.cursor()
        self.secret = "../mapserver/secret.txt"
        
    def getConnectionString(self):
        f = open (self.secret, "r")
        s = str.strip(f.readline(),'"')
        f.close()
        return s

    # def getPGConnection(self):
    #     self.conn = psycopg2.connect(getConnectionString())
    #     self.cur = self.conn.cursor()


    def getRS(self, table, column):
        # Obtiene un RS de la bd. [(nombre1, value1), ..., (nombren, valuen)]
        # Mejor obtener ambos a la vez y procesarlos para disminuir los accesos a la bd

        conn = None
        cur = None
        rs = "Error"

        try:
            conn = psycopg2.connect(self.getConnectionString())
            cur = conn.cursor()

            consult = 'SELECT nombre,' + column + ' from gis_schema.' + table + ';'
            cur.execute(consult)
            rs = cur.fetchall()
        except:
            pass
        finally:
            if cur != None:
                cur.close()
                if conn != None:
                    conn.close()
        
        return rs

    
    def string2Number(self, s):
        # puede dar problemas si acabo convirtiendo unos values a int y otros a float

        try:
            return int(s)
        except ValueError:
            pass

        try:
            return float(s)
        except ValueError:
            return "Error"
            
        

    def getValuesFromRS(self, rs):
        values = []
        for i in rs:
            values.append(self.string2Number(i[1]))


        return values

    def getNamesFromRS(self, rs):
        # los devuelve en iso8859-1
        names = []
        for i in rs:
            names.append(i[0])

        return names

    def getRangesFromValues(self, values, nranges, method):
        # nranges : numero de rangos
        # method : por si queremos implementar cuantiles, naturales, ..
        # tratar la lista ranges como range[0] <= values < range[1] ; range[n-1]<= values < range[n]
        maximum = max(values)
        minimum = min(values)
        step = int((maximum - minimum) / nranges)
        ranges = [minimum]

        for i in range(nranges):
            ranges.append(ranges[i*2]+step)
            ranges.append(ranges[i*2]+step)

        # uso como último valor del rango el máximo+1 de modo que me aseguro que todos los values 
        # + estarán por debajo
        ranges.pop()
        ranges.append(maximum+1)

        return ranges
            
       

    def getRangesFromRS(self, rs, nranges, method):
        # Devuelve un array de 10 valores con los rangos
        values = getValuesFromRS(rs, nranges, method)
        ranges = getRangesFromValues(values, nranges, method)
        return ranges

        
        
        
        
        


# dao = DAOClass();
# rs = dao.getRS("ccaa_2","pobl_2009")
# if rs != "Error":
#     values = dao.getValuesFromRS(rs)
#     print values
#     ranges = dao.getRangesFromValues(values, 5, "foo")
#     print ranges
# else:
#     print "Error"
