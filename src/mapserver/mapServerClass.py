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

import mapscript
import os
from mapFilesClass import MapFilesClass
# from scpClass import SCPClass

class MapServerClass:
    mapImageSize = "750 550"
    tbImageSize = "168 125"

    def __init__(self):
        # self.scp = SCPClass()
        self.mapfileDir = 'mapDir/' # privado
        self.imageDir = 'imageDir/' # Respecto a la parte publica del apache de abredatos
        self.mfs = MapFilesClass()
        self.host = "http://193.147.33.251"


    def generateImage(self, mapName):

        mapfilePath = os.path.abspath(self.mapfileDir + mapName + '.map')

        map = mapscript.mapObj(mapfilePath)
        mapImage = map.draw()
        imagePath = os.path.abspath(self.imageDir + mapName + '.' + mapImage.format.extension)
        mapImage.save(imagePath)
        return imagePath


    def getImageUri(self,mapName, table, column):

#        try:
        self.mfs.generateMapFile (self.mapfileDir, mapName, table, column)
        imagePath = self.generateImage(mapName)
        uri = self.host + '/srv/www/' + imagePath
        return uri
 #       except:
 # return "Error"



    # def uploadImage(self, imagePath):
    #     result = True
    #     print '1'
    #     self.scp.uploadFile(imagePath)
    #     print '2'
    #     # except Error:
    #     #   result = False
    #     #   sftp.close()
    #     #   transport.close()
    #     #   self.scp = SCPClass()
    #     # finally:
    #     #   return result



    def generateAllImages(self, mapName, table, column):
        """
        1.- Crea un .map para el mapa principal y luego la imagen (mapName.png)
        2.- Crea un .map para el thumbnail y luego el thumbnail (mapName_thumb.png)
        3.- Crea una imagen de estadísticas desde Google Chart (mapName_stats.png)
        """
        # Imagen principal
        self.mfs.generateMapFile (self.mapfileDir, mapName, table, column, self.mapImageSize )
        self.generateImage(mapName)

        # Thumbnail
        # poco optimo generar la imagen así, igual mejor con convert
        tbName = mapName + '_thumb'
        self.mfs.generateMapFile (self.mapfileDir,tbName, table, column, self.tbImageSize)
        self.generateImage(tbName)







msc = MapServerClass()

mapName = "gris_oscuro"
table = "ccaa_2"
column = "pobl_2009"

msc.generateAllImages(mapName, table, column)
#valor = msc.getImageUri(mapName, table, column)



