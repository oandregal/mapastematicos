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

class MapFilesClass:

    def getConnectionString(self):
        f = open ("secret.txt", "r")
        s = f.readline()
        f.close()
        return s


    def generateMapFile(self, mapfileDir, name, table, column):

        mapfilePath = os.path.abspath(mapfileDir + name + '.map')
        f = open (mapfilePath, "w")
        f.write ('MAP\n')
        f.write ('NAME "' + name + '"\n')
        f.write ('SIZE 400 300\n') # Tamaño en pixeles
        f.write ('IMAGECOLOR 245 245 245\n') # Color de fondo de la imagen
        f.write ('IMAGETYPE png\n')
        f.write ('EXTENT -389564.93536510505 3826792.0671249004 1127056.8418508545 4859444.06038567\n')

        f.write ('# WEB\n')
        f.write ('# TEMPLATE "/srv/www/template.html"\n') # envio la image a esta plantilla
        f.write ('# IMAGEPATH "/srv/www/images/"\n') # donde debe poner mapserver las imagenes
        f.write ('# IMAGEURL "/images/"\n') # dirige al navegador a la carpeta donde están estas imágenes.
                                          # + IMAGEPATH y IMAGEURL se refieren a la misma carpeta
                                          # + el IMAGEPATH lo procesa el CGI
                                          # + IMAGEURL lo hace el navegador.
        f.write ('# END\n') # WEB

         # Definir el shape
        f.write ('LAYER\n')
        f.write ('STATUS default\n')
        f.write ('TYPE polygon\n')
        # f.write ('LABELITEM "MASA"') # Campo del shape que contiene la etiqueta de cada feature

        f.write ('CONNECTIONTYPE POSTGIS\n')
        f.write ('CONNECTION ' + self.getConnectionString() + '\n')
        f.write ('DATA "the_geom from gis_schema.' + table +'"\n')

      # para cada rango que quiera hacer

        f.write('CLASS\n')
        f.write('STYLE \n')
        f.write('COLOR 204 255 204\n')
        f.write('OUTLINECOLOR 102 102 102\n')
        # f.write('WIDTH 1\n')
        f.write('END\n')
        f.write('EXPRESSION ([' + column + '] >= 73460 AND [' + column + '] <= 436402)\n')
        # f.write('NAME "73.460 - 436.402"\n')
        f.write('END\n')

        f.write ('CLASS\n')
        f.write ('STYLE\n')
        f.write ('COLOR 254 226 197\n') # relleno del polígono
        f.write ('OUTLINECOLOR 255 0 0\n') # color del borde
        f.write ('END\n') # STYLE
        # fin del for
        f.write ('END\n') # CLASS

        # HAY QUE PONER UN CLASS AL FINAL DEL BUCLE POR SI SE QUEDA ALGUNO FUERA

        f.write ('END\n') # LAYER


        f.write ('END\n') # NAME

        f.close()
