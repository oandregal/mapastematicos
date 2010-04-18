#! /usr/bin/env python
# -*- encoding: utf-8 -*-

# Descripcion: A partir de los datos de las tablas genera la url con los parametros del grafico de google chart y lo convierte a una imagen.

import os,string,subprocess

class GoogleChartsClass:
	
	def generateImage(self, imageDir, imageName, values, labels):
		# Definicion archivo de parametros
		param="parametros_googlechart"
	
		# Nombre imagen de salida
		# nombresalida = imageName
		imagePath=os.path.abspath(imageDir + imageName + '.png')
	
		# Titulo. [Titulo]
		titulo = ""

		# Definicion del color y el tamanho de la fuente del titulo
		colortitulo=696969	# valor de color en hexadecimal. [colorTitulo]
		fontsizetitulo=12	# valor de tamanho fuente en px. [fontsizeTitulo]

		# Tamaño del grafico. [TamanhoGrafico]
		sizegrafico='600x300'

		# Tipo de grafico, horizontal (bhs) o vertical (bvg,bvs,bvo). [TipoGrafico]
		tipografico='bhs'
		
		# Color barras. [Color]
		color='90ee90'	# valor de color en hexadecimal.

		# Lista de Valores. [Valores]
		# valores=[10,17,445,-367,98,34,-150,4,23,1,-262,-72,32,52,22,12,20,6,2]
	
		# Rango de representacion de los valores. [Rango]
		valormax=max(values)
		valormin=min(values)
		rango='%s,%s' % (valormin-20,valormax+20)

		# Labels: nombres de las CCAA/PROV. [Labels]
		# labels=["Aragon", "Asturias", "Baleares", "Canarias", "Andalucia", "Cantabria","Castilla La Mancha", "Castilla y León", "Cataluña", "Ceuta", "Com. Valenciana","Extremadura", "Galicia", "La Rioja","Madrid", "Melilla", "Murcia", "Navarra","País Vasco"]

		# ------------------------------------------

		f=open(param,'r')
		file=f.read()

		titulomod=titulo.replace(' ','+')
		labelsmod=[]
		for i in labels:
			labelsmod.append(i.replace(' ','+'))
		labelsmod='|'.join(labelsmod)
		
		
		

		replaces=[
			['[Titulo]',titulomod],
			['[colorTitulo]',colortitulo],
			['[fontsizeTitulo]',fontsizetitulo],
			['[TamanhoGrafico]',sizegrafico],
			['[TipoGrafico]',tipografico],
			['[Color]',color],
			['[Valores]',values],
			['[Rango]',rango],
			['[Labels]',labelsmod],
			#['[]',],
			[' ',''],
			['[',''],
			[']',''],
			['\'',''],
			['\n','&']
			]
	
		
		for i in replaces:
			file=file.replace(i[0],str(i[1]))
		
		# print str(values)
		# print str(labelsmod)
		# generacion de la url
		url="\"http://chart.apis.google.com/chart?"+file+"\""

		print url
		
		# curl de la url para pasar a imagen. Comando curl en bash: curl url -o imagensalida
		p=subprocess.call("curl -s %s -o %s" % (url,imagePath),shell=True)



# gc = GoogleChartsClass()
# gc.generateImage("statsDir/", "foo", )
