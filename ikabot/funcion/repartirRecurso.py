#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import traceback
from ikabot.config import *
from ikabot.helpers.botComm import *
from ikabot.helpers.pedirInfo import *
from ikabot.helpers.signals import setInfoSignal
from ikabot.helpers.getJson import getCiudad
from ikabot.helpers.planearViajes import planearViajes
from ikabot.helpers.recursos import *
from ikabot.helpers.varios import addPuntos
from ikabot.helpers.process import forkear
from ikabot.helpers.gui import banner

t = gettext.translation('repartirRecurso',
                        localedir,
                        languages=idiomas,
                        fallback=True)
_ = t.gettext

def repartirRecurso(s):

	banner()

	print(_('¿Qué recurso quiere repartir?'))
	print(_('(1) Vino'))
	print(_('(2) Marmol'))
	print(_('(3) Cristal'))
	print(_('(4) Azufre'))
	recurso = read(min=1, max=4)

	recursoTotal = 0
	dict_idVino_diponible = {}
	(idsCiudades, ciudades) = getIdsDeCiudades(s)
	ciudadesOrigen = {}
	ciudadesDestino = {}
	for idCiudad in idsCiudades:
		esTarget =  ciudades[idCiudad]['tradegood'] == str(recurso)
		if esTarget:
			html = s.get(urlCiudad + idCiudad)
			ciudad = getCiudad(html)
			ciudad['disponible'] = ciudad['recursos'][recurso]
			recursoTotal += ciudad['disponible']
			ciudadesOrigen[idCiudad] = ciudad
		else:
			html = s.get(urlCiudad + idCiudad)
			ciudad = getCiudad(html)
			ciudad['disponible'] = ciudad['libre'][recurso]
			if ciudad['disponible'] > 0:
				ciudadesDestino[idCiudad] = ciudad

	if recursoTotal == 0:
		print(_('\nNo hay recursos para enviar.'))
		enter()
		return
	if len(ciudadesDestino) == 0:
		print(_('\nNo hay espacio disponible para enviar recursos.'))
		enter()
		return

	recursoXciudad = recursoTotal // len(ciudadesDestino)
	disponibles = [ ciudadesDestino[city]['disponible'] for city in ciudadesDestino ]
	totalDisponible = sum( disponibles )
	maxDisponible = max( disponibles )
	if recursoTotal > totalDisponible:
		recursoXciudad = maxDisponible
	maximo = addPuntos(recursoXciudad)

	print(_('\nSe puede enviar como máximo {} a cada ciudad').format(maximo))
	cantidad = read(msg=_('¿Cuanto enviar a cada ciudad?:'), min=0, max=recursoXciudad)

	if cantidad == 0:
		return

	print(_('\nPor enviar {} a cada ciudad').format(addPuntos(cantidad)))
	print(_('¿Proceder? [Y/n]'))
	rta = read(values=['y', 'Y', 'n', 'N', ''])
	if rta.lower() == 'n':
		return

	forkear(s)
	if s.padre is True:
		return

	rutas = []
	for idCiudad in ciudadesDestino:
		ciudadD = ciudadesDestino[idCiudad]
		idIsla = ciudadD['islandId']
		faltante = cantidad
		for idCiudadOrigen in ciudadesOrigen:
			if faltante == 0:
				break
			ciudadO = ciudadesOrigen[idCiudadOrigen]
			recursoDisponible = ciudadO['disponible']
			for ruta in rutas:
				origen = ruta[0]
				rec = ruta[recurso + 3]
				if origen['id'] == idCiudadOrigen:
					recursoDisponible -= rec
			enviar = faltante if recursoDisponible > faltante else recursoDisponible
			disponible = ciudadD['disponible']
			if disponible < enviar:
				faltante = 0
				enviar = disponible
			else:
				faltante -= enviar

			if recurso == 1:
				ruta = (ciudadO, ciudadD, idIsla, 0, enviar, 0, 0, 0)
			elif recurso == 2:
				ruta = (ciudadO, ciudadD, idIsla, 0, 0, enviar, 0, 0)
			elif recurso == 3:
				ruta = (ciudadO, ciudadD, idIsla, 0, 0, 0, enviar, 0)
			else:
				ruta = (ciudadO, ciudadD, idIsla, 0, 0, 0, 0, enviar)
			rutas.append(ruta)

	info = _('\nRepartir recurso\n')
	for ruta in rutas:
		(ciudadO, ciudadD, idIsla, md, vn, mr, cr, az) = ruta
		rec = ruta[recurso + 3]
		info = info + _('{} -> {}\n{}: {}\n').format(ciudadO['cityName'], ciudadD['cityName'], tipoDeBien[recurso], addPuntos(rec))
	setInfoSignal(s, info)
	try:
		planearViajes(s, rutas)
	except:
		msg = _('Error en:\n{}\nCausa:\n{}').format(info, traceback.format_exc())
		sendToBot(s, msg)
	finally:
		s.logout()
