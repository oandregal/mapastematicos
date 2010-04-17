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

import mapscript
from mapFilesClass import MapFilesClass

class MapServerClass:

    def generateImage(self, mapfilePath):
        # mapfile: path to the .map file
        
        map = mapscript.mapObj(mapfilePath)
        mapImage = map.draw()
        
        imageName = 'test.' + mapImage.format.extension
        mapImage.save(imageName)

    # def uploadImage(self, imagePath):
        


  


msc = MapServerClass()
mfs = MapFilesClass()

mapfileName = "foo"
mapfilePath = "foo.map"
# mapfileName, table, colum
mfs.generateMapFile (mapfileName, "ccaa_2", "pobl_2009")
msc.generateImage (mapfilePath)
