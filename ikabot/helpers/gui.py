#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import os
import gettext
import ikabot.config as config

t = gettext.translation('gui', 
                        config.localedir, 
                        languages=config.idiomas,
                        fallback=True)
_ = t.gettext

def enter():
	getpass.getpass(_('\n[Enter]'))

def clear():
	os.system('clear')

def banner():
	clear()
	bner = """
	`7MMF'  `7MM                       `7MM\"""Yp,                 mm    
	  MM      MM                         MM    Yb                 MM    
	  MM      MM  ,MP'   ,6"Yb.          MM    dP    ,pW"Wq.    mmMMmm  
	  MM      MM ;Y     8)   MM          MM\"""bg.   6W'   `Wb     MM    
	  MM      MM;Mm      ,pm9MM          MM    `Y   8M     M8     MM    
	  MM      MM `Mb.   8M   MM          MM    ,9   YA.   ,A9     MM    
	.JMML.  .JMML. YA.  `Moo9^Yo.      .JMMmmmd9     `Ybmd9'      `Mbmo
	"""
	print('\n{}\n\n{}\n'.format(bner, config.infoUser))

class bcolors:
	HEADER = '\033[95m'
	STONE = '\033[37m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	RED = '\033[91m'
	BLACK = '\033[90m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
