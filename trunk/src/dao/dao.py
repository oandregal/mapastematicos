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

    def __init__():
        self.conn = psycopg2.connect(self.getConnectionString())
        self.cur = self.conn.cursor()

    def getConnectionString(self):
        f = open ("secret.txt", "r")
        s = f.readline()
        f.close()
        return s

    # def getPGConnection(self):
    #     self.conn = psycopg2.connect(getConnectionString())
    #     self.cur = self.conn.cursor()


    def getRS(self, table, column):
        # Obtiene un RS de la bd. [(nombre1, value1), ..., (nombren, valuen)]
        # Mejor obtener ambos a la vez y procesarlos para disminuir los accesos a la bd
        consult = 'SELECT nombre,' + column + ' from gis_schema.' + table + ';'
        cur.execute(consult)
        rs = cur.fetchall()
        return rs

    def getValuesFromRS(self, rs):
        values = []
        for i in rs:
            values.append(i[0])

        return values

    def getNamesFromRS(self, rs):
        names = []
        for i in rs:
            names.append(i[0])

        return names







    def getRanges(self, table, colunm):
        # Devuelve un array de 10 valores con los rangos
