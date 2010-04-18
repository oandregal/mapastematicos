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


# Script to clean a collection of tags in lines

cat $1 | tr ';' '\n' | tr ':' '\n' | tr ',' '\n' | tr \" ' '> /tmp/aux_123712312

python -c "

OUT = '/tmp/OUTPUT_clean.txt'

f = open('/tmp/aux_123712312' , 'rb')
f2 = open(OUT, 'wb')

lista = set()
lista2 = []
count = 0
for tag in f:
    count = count + 1
    aux = tag.rstrip().lstrip()
    lista.add(aux)
    lista2.append(aux)

f.close()
print('There was ' + str(count) + ' tags. Only ' + str(len(lista2)) +'  OK.')
print('Only ' + str(len(lista)) + ' unique tags.')
print('---> Results on file: '+ OUT)

for i in lista:
    i = i.strip()
    f2.write(i +'\n ')

f2.close()
"
rm /tmp/aux_123712312