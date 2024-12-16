#encoding: UTF-8

from PIL import ImageDraw, ImageFont, Image
from random import random
from datetime import datetime, timedelta
from time import gmtime, strftime

# definicje kolorow
bialy=(220,220,220)
zielony_j=(143,184,0)
szary=(57,75,82)
bezowy=(240,236,176)
zolty=(248,212,9)
czerwony=(228,69,40)
pomaranczowy=(204,119,34)
morski=(78,154,139)
niebieski=(6,119,176)
zielony=(67,169,33)
czarny_koliber = (11,16,19)
bialy_koliber =(223,216,223)


class dragon_renderer(abstractscreenrenderer):
	def __init__(self, lookup_path):
		self.wygaszone = self.openimage(lookup_path + "tlo")
		self.podklad = Image.open(lookup_path + "tlo1.png")
		self.lokomotywa  = Image.open(lookup_path + "lokomotywa.png")
		self.hamulce_on  = Image.open(lookup_path + "hamulce_on.png")
		self.hamulce_off  = Image.open(lookup_path + "hamulce_off.png")
		self.kabina_a  = Image.open(lookup_path + "kabina_a.png")
		self.kabina_b  = Image.open(lookup_path + "kabina_b.png")
		self.pant_a_on  = Image.open(lookup_path + "pant_a_on.png")
		self.pant_a_off  = Image.open(lookup_path + "pant_a_off.png")
		self.pant_b_on  = Image.open(lookup_path + "pant_b_on.png")
		self.pant_b_off  = Image.open(lookup_path + "pant_b_off.png")
		self.ikonki  = Image.open(lookup_path + "ikonki.png")
		self.podklad_night_koliber = self.openimage('./textures/tabor/koliber/koliber_przyciemniony')
		self.prostokat_koliber = self.openimage('./textures/tabor/koliber/koliber_prostokat')
		self.ikonka_sygnaldlugofalowy_koliber = self.openimage('./textures/tabor/koliber/koliber_ikonka_sygnaldlugofalowy')
		self.ikonka_otwartynasluch_koliber = self.openimage('./textures/tabor/koliber/koliber_ikonka_otwartynasluch')
		self.ikonka_odbiorgps_koliber = self.openimage('./textures/tabor/koliber/koliber_ikonka_odbiorgps')
		# wczytanie czcionki
		czcionka = "./fonts/framd.ttf"
		self.sredni_arial = ImageFont.truetype('./fonts/arialbd.ttf', 30)
		self.sredni_font = ImageFont.truetype(czcionka, 30)
		self.maly_font = ImageFont.truetype(czcionka, 22)
		self.bmaly_font = ImageFont.truetype(czcionka, 20)
		self.duzy_font = ImageFont.truetype(czcionka, 52)
		self.polduzy_font = ImageFont.truetype(czcionka, 36)
		self.czcionka_koliber = ImageFont.truetype('./fonts/alterebro-pixel-font-regular.ttf', 32)
		self.czcionka2_mala_koliber = ImageFont.truetype('./fonts/pixellari.ttf', 16)
		self.czcionka2_duza_koliber = ImageFont.truetype('./fonts/pixellari.ttf', 48)
		self.czcionka2_srednia_koliber = ImageFont.truetype('./fonts/pixellari.ttf', 20)
		self.czcionka2_srednia_koliber2_koliber = ImageFont.truetype('./fonts/pixellari.ttf', 24)
		
		self.kilometry = (random()*300000)+5000
		self.last_time_update = 0
		self.dzis = datetime.now().timetuple().tm_yday
		self.rok = datetime.now().year
		self.last_hour = 10
		self.temp0 = (random()*15) + 20
		self.tempM = self.temp0
		self.tempI = self.temp0
		self.tempC = self.temp0
		self.tempB = self.temp0
		self.chlodz = 0
		self.time=0
		# self.last_time_update1 = 0
		# self.lookup_path = lookup_path
		self.glosnosc = 1
		self.glosnosc_zmiana = -1
		
		
	def _render(self, state):
		#zmiana kolorów na nocne w kolibrze
		global czarny_koliber
		global bialy_koliber
		if (state['universal3']==1):
			czarny_koliber = (223,216,223)
			bialy_koliber = (11,16,19)
		else:
			czarny_koliber = (11,16,19)
			bialy_koliber = (223,216,223)
		obrazek = self.wygaszone
		dt=0
		#Prędkość
		speed = float(state['velocity'])
		if speed > 160:
			speed = 160
	
		
		if (state['cabactive'] == state['cab'] and (state['battery'] + state['converter'])):
			# kopia obrazka na potrzeby tego jednego renderowania
			obrazek = self.podklad.copy()
			# chcemy rysowac po teksturze pulpitu
			draw = ImageDraw.Draw(obrazek)
	#przyciemnienie kolibra
			if (state['universal3']==1):
				obrazek.paste(self.podklad_night_koliber,(0,778),self.podklad_night_koliber)
			zmienna_kanalu = str(state['radio_channel'])
	#prędkość zadana wskaz
			tempomat = state['speedctrl']
			if (tempomat > 0):
				rotate = tempomat * 256 / 160 -128
				rad =  radians(rotate)
				srodek = (234, 305)
				point = (0,-172)
				p1 = (srodek[0]+point[0]*cos(rad)-point[1]*sin(rad),srodek[1]+point[1]*cos(rad)+point[0]*sin(rad))
				point = (-21,-238)
				p2 = (srodek[0]+point[0]*cos(rad)-point[1]*sin(rad),srodek[1]+point[1]*cos(rad)+point[0]*sin(rad))
				point = (21,-238)
				p3 = (srodek[0]+point[0]*cos(rad)-point[1]*sin(rad),srodek[1]+point[1]*cos(rad)+point[0]*sin(rad))
				draw.polygon([p1,p2,p3],fill=zielony_j)
	#prędkościomierz
			tacho=bialy
			if (tempomat > 0)&(speed > tempomat+0.5):
				tacho=czerwony
			draw.ellipse([(177, 248), (291, 362)], fill=tacho)
			rotate = speed * 256 / 160 + 52
			rad =  radians(rotate)
			srodek_tacho = (234, 305)
			point = (-14,52)
			p1 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (14,52)
			p2 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (4,234)
			p3 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (-4,234)
			p4 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			draw.polygon([p1,p2,p3,p4],fill=tacho)
	#słupki
			#prędkość wartość
			self.print_center(draw, '%d' % speed, 234, 284, self.sredni_font, szary)
			self.print_center(draw, '%d' % speed, 234, 31, self.duzy_font, bialy)
			self.print_center(draw, '%d' % speed, 234, 1308, self.duzy_font, bialy)
			
			#prędkość zadana wartość
			if (tempomat > 0):
				self.print_center(draw, '%d' % tempomat, 234, 330, self.sredni_font, zielony_j)
			
			#moment zadany
			mz = state['eimp_t_pdt']*100
			pos = 427 - (mz * 2.82)
			draw.rectangle((492,427,532,pos), fill=morski)
			self.print_center(draw, '%d' % mz, 512, 452, self.maly_font, bialy)
			#moment realizowany
			mr = state['eimp_c1_prt']*100
			pos = 427 - (mr * 2.82)
			draw.rectangle((568,427,608,pos), fill=niebieski)
			self.print_center(draw, '%d' % mr, 588, 452, self.maly_font, bialy)
			#napięcie sieci
			us = state['eimp_c1_uhv']
			self.print_center(draw, '%d' % us, 665, 452, self.maly_font, bialy)
			if us>4000:
				us=4000
			pos = 427 - (us * 0.0705)
			draw.rectangle((645,427,685,pos), fill=bezowy)
			#prąd sumaryczny
			prad = state['eimp_c1_ihv']
			if prad<0:
				prad=0
			pos = 427 - (prad * 0.141)
			draw.rectangle((721,427,761,pos), fill=pomaranczowy)
			self.print_center(draw, '%.0f' % prad, 741, 452, self.maly_font, bialy)
			#napięcie baterii
			cv = state['eimp_c1_cv']
			pos = 427 - (cv * 1.88)
			draw.rectangle((797,427,837,pos), fill=zielony_j)
			self.print_center(draw, '%.0f' % cv, 817, 452, self.maly_font, bialy)
			#PG
			bp = state['eimp_pn1_bp']
			pos = 427 - (bp * 23.5)
			draw.rectangle((873,427,913,pos), fill=zolty)
			self.print_center(draw, '%.1f' % bp, 893, 452, self.maly_font, bialy)
			#PZ
			sp = state['eimp_pn1_sp']
			pos = 427 - (sp * 23.5)
			draw.rectangle((949,427,989,pos), fill=czerwony)
			self.print_center(draw, '%.1f' % sp, 969, 452, self.maly_font, bialy)
			
	#ikona lokomotywy
			obrazek.paste(self.lokomotywa,(4,545),self.lokomotywa)
			if state['dir_brake'] or state['indir_brake']:#hamulec
				obrazek.paste(self.hamulce_on,(4,545),self.hamulce_on)
			else:
				obrazek.paste(self.hamulce_off,(4,545),self.hamulce_off)
			if state['cab'] == 1:
				obrazek.paste(self.kabina_a,(4,545),self.kabina_a)
			if state['cab'] == -1:
				obrazek.paste(self.kabina_b,(4,545),self.kabina_b)
			if state['eimp_u1_pf']:
				obrazek.paste(self.pant_a_on,(4,545),self.pant_a_on)
			else:
				obrazek.paste(self.pant_a_off,(4,545),self.pant_a_off)
			if state['eimp_u1_pr']:
				obrazek.paste(self.pant_b_on,(4,545),self.pant_b_on)
			else:
				obrazek.paste(self.pant_b_off,(4,545),self.pant_b_off)
	#podświetlenia tabelki
			if state['eimp_c1_conv']:#przetwornica
				draw.rectangle((629,469,705,543), fill=zielony)
			if state['eimp_c1_conv']:#WCH P
				draw.rectangle((707,469,781,543), fill=zielony_j)
			if state['eimp_c1_ms']:#silniki
				draw.rectangle((782,469,856,543), fill=zielony_j)
			if state['eimp_c1_conv']:#WCH W
				draw.rectangle((858,469,933,543), fill=zielony_j)
			if state['pant_compressor']:#sprężarka pomocnicza
				draw.rectangle((478,469,551,543), fill=zielony_j)
			if state['eimp_c1_ms']:#WS
				draw.rectangle((553,469,628,543), fill=zielony_j)
			elif state['main_ready']:
				draw.rectangle((553,469,628,543), fill=zolty)
			else:
				if ((state['seconds'] % 2) == 1):
					draw.rectangle((553,469,628,543), fill=zolty)
			if (state['fuse'] or state['converter_overload']):#alarm
				draw.rectangle((935,469,1008,543), fill=czerwony)
			if state['eimp_u1_comp_w']:#sprężarki
				draw.rectangle((478,546,628,620), fill=zielony_j)
			if ((state['dir_brake'] or state['indir_brake']) and ((state['eimp_c1_prt'] > 0) and (state['eimp_c1_im'] > 5))):#hamulec awaria
				draw.rectangle((629,546,706,620), fill=czerwony)
			if (state['brakes_1_spring_active']):#hamulec postojowy
				draw.rectangle((709,546,779,620), fill=czerwony)
			if state['eimp_c1_conv']:#chłodzenie silników
				draw.rectangle((858,546,934,620), fill=zielony_j)
			#if (state['eimp_c1_frb'] > 0.1):#chłodzenie rezystorów hamowania
			if (self.chlodz == 1):
				draw.rectangle((935,546,1009,620), fill=zielony_j)
			
	#ikonki w tabelce
			obrazek.paste(self.ikonki,(476,467),self.ikonki)
			
	#napisy
			# czas
			if state['seconds'] != self.last_time_update:
				dt = state['seconds'] - self.last_time_update
				if dt < 0:
					dt+=60
				self.kilometry += dt*speed * 0.0002778
				self.last_time_update = state['seconds']
				self.time=self.time+1
			czas = str(state['hours']) + ":" 
			if state['minutes']<10:
				czas = czas + "0" + str(state['minutes']) + ":"
			else:
				czas = czas + str(state['minutes']) + ":"
			if state['seconds']<10:
				czas = czas + "0" +str(state['seconds'])
			else:
				czas = czas + str(state['seconds'])
			godzina_koliber = czas	
			czas = czas + " / 5"
			self.print_center(draw, czas, 75,54, self.bmaly_font, bialy)
			self.print_center(draw, czas, 75,1331, self.bmaly_font, bialy)
			
			# data
			if self.last_hour == 23 and state['hours'] == 0:
				self.dzis = self.dzis+1 # wlasnie wybila polnoc
			self.last_hour = state['hours']
			data = datetime(self.rok, 1, 1) + timedelta(self.dzis - 1)
			data = data.strftime("%d/%m/%Y") 
			self.print_center(draw, data, 75,28, self.bmaly_font, bialy)
			self.print_center(draw, data, 75,1305, self.bmaly_font, bialy)
			
			self.print_center(draw, 'JAZDA', 232,495, self.sredni_arial, bialy)
			if state['direction'] == 1:
				self.print_center(draw, u'PRZóD', 232,524, self.sredni_arial, bialy)
			if state['direction'] == -1:
				self.print_center(draw, u'TYŁ', 232,524, self.sredni_arial, bialy)
			
			
			self.print_center(draw, str(int(self.kilometry)), 821,655, self.polduzy_font, bialy)
			
		# tabelki pomiarów
			# temp łożysk lewych
			speed = float(state['velocity'])
			self.tempB = self.tempB + ((self.temp0 - self.tempB) * 0.00002 + (speed*0.000009)) * dt
			self.print_center(draw, '%d' % self.tempB, 428,1475, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 533,1475, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 638,1475, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 743,1475, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 848,1475, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 953,1475, self.bmaly_font, bialy)
			#temp łożysk prawych
			self.print_center(draw, '%d' % self.tempB, 428,1507, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 533,1507, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 638,1507, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 743,1507, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 848,1507, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempB, 953,1507, self.bmaly_font, bialy)
			#prędkości osi
			self.print_center(draw, '%d' % speed, 428,1539, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % speed, 533,1539, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % speed, 638,1539, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % speed, 743,1539, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % speed, 848,1539, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % speed, 953,1539, self.bmaly_font, bialy)
			#temperatury silników
			im = abs(state['eimp_c1_im'])
			self.tempM = self.tempM + ((self.temp0 - self.tempM) * 0.0005 + (im * im) * 0.0000012) * dt
			self.print_center(draw, '%d' % self.tempM, 428,1600, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempM, 533,1600, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempM, 638,1600, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempM, 743,1600, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempM, 848,1600, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempM, 953,1600, self.bmaly_font, bialy)
			#procent momentu silników
			self.print_center(draw, '%d' % mr, 428,1631, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % mr, 533,1631, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % mr, 638,1631, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % mr, 743,1631, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % mr, 848,1631, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % mr, 953,1631, self.bmaly_font, bialy)
			#prąd silników
			im = state['eimp_c1_im']
			self.print_center(draw, '%d' % im, 428,1662, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % im, 533,1662, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % im, 638,1662, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % im, 743,1662, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % im, 848,1662, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % im, 953,1662, self.bmaly_font, bialy)
			#temp faliwnika 1
			ihv = abs(state['eimp_c1_ihv'])
			self.tempI = self.tempI + ((self.temp0 - self.tempI) * 0.0005 + (ihv * ihv) * 0.000000012) * dt
			self.print_center(draw, '%d' % self.tempI, 596,1724, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempI, 755,1724, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempI, 914,1724, self.bmaly_font, bialy)
			#temp falownika 2
			self.print_center(draw, '%d' % self.tempI, 596,1755, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempI, 755,1755, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempI, 914,1755, self.bmaly_font, bialy)
			#temp czopera
			if state['eimp_c1_im'] < 0:
				ih = state['eimp_c1_im']
			else:
				ih = 0
			# chlodzenie 0.006
			if self.tempC > 500:
				self.chlodz = 1
			if self.tempC < 200:
				self.chlodz = 0
			self.tempC = self.tempC + (((self.temp0 - self.tempC) * (0.0002+(0.006*self.chlodz))) + (ih * ih) * 0.00008) * dt
			self.print_center(draw, '%d' % self.tempC, 596,1786, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempC, 755,1786, self.bmaly_font, bialy)
			self.print_center(draw, '%d' % self.tempC, 914,1786, self.bmaly_font, bialy)
			#napięcie baterii
			self.print_center(draw, '%d' % cv, 874,1846, self.bmaly_font, bialy)
			
			# if state['seconds'] != self.last_time_update1:
				# self.last_time_update1 = state['seconds']
				# self.time=self.time+1
				# with open(self.lookup_path + "termometry.txt", 'a') as temp_file:
					# temp_file.write(str(self.time)+' '+str('%.2f' % speed)+' '+str('%.2f' % im)+' '+str('%.2f' % self.tempB)+' '+str('%.2f' % self.tempM)+' '+str('%.2f' % self.tempI)+' '+str('%.2f' % self.tempC)+'\n')
			
			
			#RADIOTELEFON
			
			#napis kanal maly
			draw.text((3,805), u'KANAL', font=self.czcionka2_mala_koliber, fill=czarny_koliber)
			
			#dolne napisy
			draw.text((22,882), u'ZEW 1', font=self.czcionka2_srednia_koliber, fill=czarny_koliber)
			draw.text((122,882), u'ZEW 3', font=self.czcionka2_srednia_koliber, fill=czarny_koliber)
			draw.text((211,882), u'NASLUCH', font=self.czcionka2_srednia_koliber, fill=czarny_koliber)
			draw.text((331,882), u'SZUM', font=self.czcionka2_srednia_koliber, fill=czarny_koliber)
			draw.text((433,882), u'MENU', font=self.czcionka2_srednia_koliber, fill=czarny_koliber)
		
			#zegarynka
			draw.text((441,776), godzina_koliber, fill=czarny_koliber, font=self.czcionka_koliber)
		
			#pokazanie numeru kanalu
			if state['radio_channel'] < 10:
				draw.text((60,802), "00"+ zmienna_kanalu, font=self.czcionka2_duza_koliber, fill=czarny_koliber)
		
			if state['radio_channel'] > 9:
				draw.text((60,802), "0"+ zmienna_kanalu, font=self.czcionka2_duza_koliber, fill=czarny_koliber)
			
			if state['radio_channel'] < 8:
				draw.text((150,822), "Pociagowy R"+ zmienna_kanalu, font=self.czcionka2_srednia_koliber2_koliber, fill=czarny_koliber)
		
			if (state['radio_channel']==8):
				draw.text((150,822), u'Ratunkowy', font=self.czcionka2_srednia_koliber2_koliber, fill=czarny_koliber)
			
			if (state['radio_channel']==9):
				draw.text((150,822), u'Manewrowy', font=self.czcionka2_srednia_koliber2_koliber, fill=czarny_koliber)
			
			if (state['radio_channel']==10):
				draw.text((150,822), u'Radiostop', font=self.czcionka2_srednia_koliber2_koliber, fill=czarny_koliber)
				
			#pokazanie glosnosci jesli zmieniona
			if state["radio_volume"] != self.glosnosc:
				self.glosnosc = state["radio_volume"]
				self.glosnosc_zmiana = state["seconds"]
			
			if self.glosnosc_zmiana != -1:
				draw.text((3, 852), u"GŁOŚNOŚĆ", font=self.czcionka2_srednia_koliber2_koliber, fill=czarny_koliber)
				draw.rectangle(((135, 854), (508, 870)), fill = czarny_koliber)
				draw.rectangle(((138, 857), (505, 867)), fill = bialy_koliber)
				draw.rectangle(((135, 854), (135 + (373 * self.glosnosc), 870)), fill = czarny_koliber)
				if (state["seconds"] - self.glosnosc_zmiana) % 60 == 3:
					self.glosnosc_zmiana = -1
			778
			#rysowanie prostokat_koliberow
			draw.bitmap((3,878), bitmap=self.prostokat_koliber ,fill=czarny_koliber)
			draw.bitmap((105,878), bitmap=self.prostokat_koliber ,fill=czarny_koliber)
			draw.bitmap((207,878), bitmap=self.prostokat_koliber ,fill=czarny_koliber)
			draw.bitmap((310,878), bitmap=self.prostokat_koliber ,fill=czarny_koliber)
			draw.bitmap((412,878), bitmap=self.prostokat_koliber ,fill=czarny_koliber)
		
			#rysowanie ikonek
			draw.bitmap((207,780), bitmap=self.ikonka_otwartynasluch_koliber ,fill=czarny_koliber)
			draw.bitmap((290,780), bitmap=self.ikonka_odbiorgps_koliber ,fill=czarny_koliber)
			draw.bitmap((320,780), bitmap=self.ikonka_sygnaldlugofalowy_koliber ,fill=czarny_koliber)
			
		return obrazek
