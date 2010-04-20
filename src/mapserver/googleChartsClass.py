#! /usr/bin/env python
# -*- encoding: utf-8 -*-

# Descripcion: A partir de los datos de las tablas genera la url con los parametros del grafico de google chart y lo convierte a una imagen.

# TODO: 
# + Improve how values is handled through the app, when it must be a str and when a number

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
		# Labels: nombres de las CCAA/PROV. [Labels]
 		my_values = list()
 		my_labels = list()

 		for i in range(0,len(values)):
 			n = self.string2Number(values[i])
 			if n != None:
 				my_values.append(n)
 				my_labels.append(labels[i])
				
		values = my_values
		my_labels.reverse() # gcharts reverse the order
		labels = my_labels

	
		# Rango de representacion de los valores. [Rango]
		valormax=max(values)
		valormin=min(values)
		rango='%s,%s' % (valormin-20,valormax+20)



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
		
		# generacion de la url
		url="\"http://chart.apis.google.com/chart?"+file+"\""

		
		# curl de la url para pasar a imagen. Comando curl en bash: curl url -o imagensalida
		p=subprocess.call("curl -s %s -o %s" % (url,imagePath),shell=True)


	def string2Number(self, s):
				
 		try:
 			return int(s)
 		except ValueError:
 			pass
 		
		try:
 			return float(s)
 		except ValueError:
 			return None

# gc = GoogleChartsClass()

# values = [10,17,445,-367,98,34,-150,4,23,1,-262,-72,32,52,22,12,20,6,2]
# labels=["Aragon", "Asturias", "Baleares", "Canarias", "Andalucia", "Cantabria","Castilla La Mancha", "Castilla y León", "Cataluña", "Ceuta", "Com. Valenciana","Extremadura", "Galicia", "La Rioja","Madrid", "Melilla", "Murcia", "Navarra","País Vasco"]

# gc.generateImage("statsDir/", "foo", values, labels)

