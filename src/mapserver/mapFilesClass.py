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

import os
from dao import DAOClass

class MapFilesClass:

    NRANGES = 5

    def __init__(self):
        self.dao = DAOClass();

    def getConnectionString(self):
        f = open ("secret.txt", "r")
        s = f.readline()
        f.close()
        return s

    def getRanges(self, table, column):
        rs = self.dao.getRS(table,column)
        
        
        if rs != "Error":
            values = self.dao.getValuesFromRS(rs)
            ranges = self.dao.getRangesFromValues(values, self.NRANGES, "foo")

            print rs
            print ranges

            return ranges
        else:
            print "Error Accediendo a la bd"

            
    def getRangeN(self, ranges, n):
        return ranges[n*2:n*2+2]
    
    
    def generateMapFile(self, mapfileDir, name, table, column):
        
        ranges = self.getRanges(table, column)

        

        mapfilePath = os.path.abspath(mapfileDir + name + '.map')
        f = open (mapfilePath, "w")
        f.write ('MAP\n')
        f.write ('NAME "' + name + '"\n')
        f.write ('SIZE 400 300\n') # Tamaño en pixeles
        f.write ('IMAGECOLOR 245 245 245\n') # Color de fondo de la imagen
        f.write ('IMAGETYPE png\n')
        f.write ('EXTENT -389564.93536510505 3826792.0671249004 1127056.8418508545 4859444.06038567\n')

         # Definir el shape
        f.write ('LAYER\n')
        f.write ('STATUS default\n')
        f.write ('TYPE polygon\n')
        # f.write ('LABELITEM "MASA"') # Campo del shape que contiene la etiqueta de cada feature

        f.write ('CONNECTIONTYPE POSTGIS\n')
        f.write ('CONNECTION ' + self.getConnectionString() + '\n')
        f.write ('DATA "the_geom from gis_schema.' + table +'"\n')

      # para cada rango que quiera hacer
        for i in range(self.NRANGES):
            f.write('CLASS\n')
            f.write('STYLE \n')
            f.write('COLOR ' + self.dao.color[i] + '\n')
            f.write('OUTLINECOLOR 105 105 105\n')
            f.write('END\n')
            limits = self.getRangeN(ranges, i)
            f.write('EXPRESSION ([' + column + '] >= ' + str(limits[0]) + ' AND [' + column + '] <= ' + str(limits[1]) + ')\n')
            f.write('END\n') # CLASS


        # un class al final de todo por si alguno se queda fuera.
        # + con este definimos además el color del borde de los polígonos
        f.write ('CLASS\n')
        f.write ('STYLE\n')
        f.write ('COLOR 255 255 255\n')
        f.write ('OUTLINECOLOR 105 105 105\n')
        f.write ('END\n') # STYLE
        f.write ('END\n') # CLASS


        f.write ('END\n') # LAYER

        f.write ('END\n') # MAP

        f.close()
