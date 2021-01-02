# ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# Copyright 2021 Jochen Schmähling
# ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
#  Python Module for communication with viControl heatings using the serial Optolink interface
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
# ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

import logging

controlset = {
    'Baudrate': 4800,
    'Bytesize': 8,          # 'EIGHTBITS'
    'Parity': 'E',          # 'PARITY_EVEN',
    'Stopbits': 2,          # 'STOPBITS_TWO',
}



commandset = {
    # generelle Infos
    'Anlagentyp': {'addr': '00F8', 'len': 2, 'unit': 'DT', 'set': False},
    # getAnlTyp -- Information - Allgemein: Anlagentyp (204D)
    'Aussentemperatur': {'addr': '0101', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempA -- Information - Allgemein: Aussentemperatur (-40..70)

    # Anlagenstatus
    'Betriebsart': {'addr': 'B000', 'len': 1, 'unit': 'BA', 'set': True},
    # getBetriebsart -- Bedienung HK1 - Heizkreis 1: Betriebsart (Textstring)
    'Manuell': {'addr': 'B020', 'len': 1, 'unit': 'IUNON', 'set': True, 'min_value': 0, 'max_value': 2},
    # getManuell / setManuell -- 0 = normal, 1 = manueller Heizbetrieb, 2 = 1x Warmwasser auf Temp2
    'Sekundaerpumpe': {'addr': '0484', 'len': 1, 'unit': 'RT', 'set': False},
    # getStatusSekP -- Diagnose - Anlagenuebersicht: Sekundaerpumpe 1 (0..1)
    'Heizkreispumpe': {'addr': '048D', 'len': 1, 'unit': 'RT', 'set': False},
    # getStatusPumpe -- Information - Heizkreis HK1: Heizkreispumpe (0..1)
    'Zirkulationspumpe': {'addr': '0490', 'len': 1, 'unit': 'RT', 'set': False},
    # getStatusPumpeZirk -- Information - Warmwasser: Zirkulationspumpe (0..1)
    'VentilHeizenWW': {'addr': '0494', 'len': 1, 'unit': 'RT', 'set': False},
    # getStatusVentilWW -- Diagnose - Waermepumpe: 3-W-Ventil Heizen WW1 (0 (Heizen)..1 (WW))
    'Vorlaufsolltemp': {'addr': '1800', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempVLSoll -- Diagnose - Heizkreis HK1: Vorlaufsolltemperatur HK1 (0..95)
    'Outdoor_Fanspeed': {'addr': '1A52', 'len': 1, 'unit': 'IUNON', 'set': False},  # getSpdFanOut -- Outdoor Fanspeed
    'Status_Fanspeed': {'addr': '1A53', 'len': 1, 'unit': 'IUNON', 'set': False},
    # getSpdFan -- Geschwindigkeit Luefter
    'Kompressor_Freq': {'addr': '1A54', 'len': 1, 'unit': 'IUNON', 'set': False},  # getSpdKomp -- Compressor Frequency

    # Temperaturen
    'SolltempWarmwasser': {'addr': '6000', 'len': 2, 'unit': 'IS10', 'set': True, 'min_value': 10, 'max_value': 60},
    # getTempWWSoll -- Bedienung WW - Betriebsdaten WW: Warmwassersolltemperatur (10..60 (95))
    'VorlauftempSek': {'addr': '0105', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempSekVL -- Information - Heizkreis HK1: Vorlauftemperatur Sekundaer 1 (0..95)
    'RuecklauftempSek': {'addr': '0106', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempSekRL -- Diagnose - Anlagenuebersicht: Ruecklauftemperatur Sekundaer 1 (0..95)
    'Warmwassertemperatur': {'addr': '010d', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempWWIstOben -- Information - Warmwasser: Warmwassertemperatur oben (0..95)

    # Stellwerte
    'Raumsolltemp': {'addr': '2000', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempRaumSollNormal -- Bedienung HK1 - Heizkreis 1: Raumsolltemperatur normal (10..30)
    'RaumsolltempReduziert': {'addr': '2001', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempRaumSollRed -- Bedienung HK1 - Heizkreis 1: Raumsolltemperatur reduzierter Betrieb (10..30)
    'HeizkennlinieNiveau': {'addr': '2006', 'len': 2, 'unit': 'IS10', 'set': False},
    # getHKLNiveau -- Bedienung HK1 - Heizkreis 1: Niveau der Heizkennlinie (-15..40)
    'HeizkennlinieNeigung': {'addr': '2007', 'len': 2, 'unit': 'IS10', 'set': False},
    # getHKLNeigung -- Bedienung HK1 - Heizkreis 1: Neigung der Heizkennlinie (0..35)
    'RaumsolltempParty': {'addr': '2022', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempRaumSollParty -- Bedienung HK1 - Heizkreis 1: Party Solltemperatur (10..30)

    # Statistiken / Laufzeiten
    'EinschaltungenSekundaer': {'addr': '0504', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getAnzQuelleSek -- Statistik - Schaltzyklen Anlage: Einschaltungen Sekundaerquelle (?)
    'EinschaltungenHeizstab1': {'addr': '0508', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getAnzHeizstabSt1 -- Statistik - Schaltzyklen Anlage: Einschaltungen Heizstab Stufe 1 (?)
    'EinschaltungenHeizstab2': {'addr': '0509', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getAnzHeizstabSt2 -- Statistik - Schaltzyklen Anlage: Einschaltungen Heizstab Stufe 2 (?)
    'EinschaltungenHK': {'addr': '050D', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getAnzHK -- Statistik - Schaltzyklen Anlage: Einschaltungen Heizkreis (?)
    'LZSekundaerpumpe': {'addr': '0584', 'len': 4, 'unit': 'IU3600', 'set': False},
    # getLZPumpeSek -- Statistik - Betriebsstunden Anlage: Betriebsstunden Sekundaerpumpe (?)
    'LZHeizstab1': {'addr': '0588', 'len': 4, 'unit': 'IU3600', 'set': False},
    # getLZHeizstabSt1 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Heizstab Stufe 1 (?)
    'LZHeizstab2': {'addr': '0589', 'len': 4, 'unit': 'IU3600', 'set': False},
    # getLZHeizstabSt2 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Heizstab Stufe 2 (?)
    'LZPumpeHK': {'addr': '058D', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getLZPumpe -- Statistik - Betriebsstunden Anlage: Betriebsstunden Pumpe HK1 (0..1150000)
    'LZWWVentil': {'addr': '0594', 'len': 4, 'unit': 'IU3600', 'set': False},
    # getLZVentilWW -- Statistik - Betriebsstunden Anlage: Betriebsstunden Warmwasserventil (?)
    'LZVerdichterStufe1': {'addr': '1620', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getLZVerdSt1 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 1 (?)
    'LZVerdichterStufe2': {'addr': '1622', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getLZVerdSt2 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 2 (?)
    'LZVerdichterStufe3': {'addr': '1624', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getLZVerdSt3 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 3 (?)
    'LZVerdichterStufe4': {'addr': '1626', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getLZVerdSt4 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 4 (?)
    'LZVerdichterStufe5': {'addr': '1628', 'len': 4, 'unit': 'IUNON', 'set': False},
    # getLZVerdSt5 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 5 (?)
    'VorlauftempSekMittel': {'addr': '16B2', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempSekVLMittel -- Statistik - Energiebilanz: mittlere sek. Vorlauftemperatur (0..95)
    'RuecklauftempSekMittel': {'addr': '16B3', 'len': 2, 'unit': 'IS10', 'set': False},
    # getTempSekRLMittel -- Statistik - Energiebilanz: mittlere sek.Temperatur RL1 (0..95)
    'OAT_Temperature': {'addr': '1A5C', 'len': 1, 'unit': 'IUNON', 'set': False},  # getTempOAT -- OAT Temperature
    'ICT_Temperature': {'addr': '1A5D', 'len': 1, 'unit': 'IUNON', 'set': False},  # getTempICT -- OCT Temperature
    'CCT_Temperature': {'addr': '1A5E', 'len': 1, 'unit': 'IUNON', 'set': False},  # getTempCCT -- CCT Temperature
    'HST_Temperature': {'addr': '1A5F', 'len': 1, 'unit': 'IUNON', 'set': False},  # getTempHST -- HST Temperature
    'OMT_Temperature': {'addr': '1A60', 'len': 1, 'unit': 'IUNON', 'set': False},  # getTempOMT -- OMT Temperature
    'LZVerdichterWP': {'addr': '5005', 'len': 4, 'unit': 'IU3600', 'set': False},
    # getLZWP -- Statistik - Betriebsstunden Anlage: Betriebsstunden Waermepumpe  (0..1150000)
    'SollLeistungVerdichter': {'addr': '5030', 'len': 1, 'unit': 'IUNON', 'set': False},
    # getPwrSollVerdichter -- Diagnose - Anlagenuebersicht: Soll-Leistung Verdichter 1 (0..100)
    'WaermeWW12M': {'addr': '1660', 'len': 4, 'unit': 'IU10', 'set': False},
    # Wärmeenergie für WW-Bereitung der letzten 12 Monate (kWh)
    'ElektroWW12M': {'addr': '1670', 'len': 4, 'unit': 'IU10', 'set': False},
    # elektr. Energie für WW-Bereitung der letzten 12 Monate (kWh)
    'WWeinmal':{'addr':'xxxx','len':1,'unit':'OO','set':True}
}


class viCommand(bytearray):
    # the commands
    # viCommand object value is a bytearray of addr and len

    Command_bytes_read = 5 # addr (2 bytes),
    Command_bytes_write = 5


    def __init__(self,cmdname):
        # FIXME: Error handling if command name is not found
        cs=commandset[cmdname]
        self.__cmdcode__=cs['addr']
        self.__valuebytes__=cs['len']
        self.unit=cs['unit']
        self.set=cs['set']
        self.cmdname=cmdname

        #create bytearray representation
        b=bytes.fromhex(self.__cmdcode__)+self.__valuebytes__.to_bytes(1,'big')
        super().__init__(b)

    @classmethod
    def frombytes(cls,b:bytearray):
        #create command from addr given as byte
        #only the first two bytes of b are evaluated
        try:
            logging.debug(f'Convert {b.hex()} to command')
            cmdname=next(key for key, value in commandset.items() if value['addr'].lower() == b[0:2].hex())
        except:
            raise Exception(f'No Command matching {b[0:2].hex()}')
        return viCommand(cmdname)

    def responselen(self):
        #returns the number of bytes in the response
        # 4 is the response header length, see protocommandset
        return self.__valuebytes__+4+self.Command_bytes_read

class viProtocmd(bytearray):
    # bytearray representation of proto-commands
    protocmdset = {
        # the strings are hex numbers and can be converted using bytearray.fromhex(...)
        # length in bytes is then available via 'len' function
        #FIXME keine Strings sondern byte-werte
        #FIXME: die werte unten könnten auf die verschiedenen Klassen aufgeteilt werden.
        #fixme: definition als lower case
        'StartByte': '41',
        'Request': '00',
        'Response': '01',
        'Error': '03',
        'Read': '01',
        'Write': '02',
        'Function_Call': '07',
        'Acknowledge': '06',
        'Not_initiated': '05',
        'Init_Error': '15',
        'Reset_Command': '04',
        'Reset_Command_Response': '05',
        'Sync_Command': '160000',
        'Sync_Command_Response': '06',
        # init:              send'Reset_Command' receive'Reset_Command_Response' send'Sync_Command'
        # request:           send('StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Request' 'Read' 'addr' 'checksum')
        # request_response:  receive('Acknowledge' 'StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Response' 'Read' 'addr' 'Anzahl der Bytes des Wertes' 'Wert' 'checksum')
    }

    def __init__(self,cmd):
        #if cmd is a string return protocommand code
        if type(cmd)==str:
            #FIXME das muss auch schöner gehen
            super().__init__(0)
            super().extend(bytes.fromhex(self.protocmdset[cmd]))
        elif type(cmd)==int:
            # else, convert int to byte representation
            super.__init__(cmd.to_bytes(1,'big'))
        elif type(cmd)==bytes or type(cmd)==bytearray:
            #pass raw data
            super().__init__(cmd)


errorset = {
    '00': 'Regelbetrieb (kein Fehler)',
    '0F': 'Wartung (fuer Reset Codieradresse 24 auf 0 stellen)',
    '10': 'Kurzschluss Aussentemperatursensor',
    '18': 'Unterbrechung Aussentemperatursensor',
    '20': 'Kurzschluss Vorlauftemperatursensor',
    '21': 'Kurzschluss Ruecklauftemperatursensor',
    '28': 'Unterbrechung Aussentemperatursensor',
    '29': 'Unterbrechung Ruecklauftemperatursensor',
    '30': 'Kurzschluss Kesseltemperatursensor',
    '38': 'Unterbrechung Kesseltemperatursensor',
    '40': 'Kurzschluss Vorlauftemperatursensor M2',
    '42': 'Unterbrechung Vorlauftemperatursensor M2',
    '50': 'Kurzschluss Speichertemperatursensor',
    '58': 'Unterbrechung Speichertemperatursensor',
    '92': 'Solar: Kurzschluss Kollektortemperatursensor',
    '93': 'Solar: Kurzschluss Sensor S3',
    '94': 'Solar: Kurzschluss Speichertemperatursensor',
    '9A': 'Solar: Unterbrechung Kollektortemperatursensor',
    '9B': 'Solar: Unterbrechung Sensor S3',
    '9C': 'Solar: Unterbrechung Speichertemperatursensor',
    '9E': 'Solar: Zu geringer bzw. kein Volumenstrom oder Temperaturwächter ausgeloest',
    '9F': 'Solar: Fehlermeldung Solarteil (siehe Solarregler)',
    'A7': 'Bedienteil defekt',
    'B0': 'Kurzschluss Abgastemperatursensor',
    'B1': 'Kommunikationsfehler Bedieneinheit',
    'B4': 'Interner Fehler (Elektronik)',
    'B5': 'Interner Fehler (Elektronik)',
    'B6': 'Ungueltige Hardwarekennung (Elektronik)',
    'B7': 'Interner Fehler (Kesselkodierstecker)',
    'B8': 'Unterbrechung Abgastemperatursensor',
    'B9': 'Interner Fehler (Dateneingabe wiederholen)',
    'BA': 'Kommunikationsfehler Erweiterungssatz fuer Mischerkreis M2',
    'BC': 'Kommunikationsfehler Fernbedienung Vitorol, Heizkreis M1',
    'BD': 'Kommunikationsfehler Fernbedienung Vitorol, Heizkreis M2',
    'BE': 'Falsche Codierung Fernbedienung Vitorol',
    'C1': 'Externe Sicherheitseinrichtung (Kessel kuehlt aus)',
    'C2': 'Kommunikationsfehler Solarregelung',
    'C5': 'Kommunikationsfehler drehzahlgeregelte Heizkreispumpe, Heizkreis M1',
    'C6': 'Kommunikationsfehler drehzahlgeregelte Heizkreispumpe, Heizkreis M2',
    'C7': 'Falsche Codierung der Heizkreispumpe',
    'C9': 'Stoermeldeeingang am Schaltmodul-V aktiv',
    'CD': 'Kommunikationsfehler Vitocom 100 (KM-BUS)',
    'CE': 'Kommunikationsfehler Schaltmodul-V',
    'CF': 'Kommunikationsfehler LON Modul',
    'D1': 'Brennerstoerung',
    'D4': 'Sicherheitstemperaturbegrenzer hat ausgeloest oder Stoermeldemodul nicht richtig gesteckt',
    'DA': 'Kurzschluss Raumtemperatursensor, Heizkreis M1',
    'DB': 'Kurzschluss Raumtemperatursensor, Heizkreis M2',
    'DD': 'Unterbrechung Raumtemperatursensor, Heizkreis M1',
    'DE': 'Unterbrechung Raumtemperatursensor, Heizkreis M2',
    'E4': 'Fehler Versorgungsspannung',
    'E5': 'Interner Fehler (Ionisationselektrode)',
    'E6': 'Abgas- / Zuluftsystem verstopft',
    'F0': 'Interner Fehler (Regelung tauschen)',
    'F1': 'Abgastemperaturbegrenzer ausgeloest',
    'F2': 'Temperaturbegrenzer ausgeloest',
    'F3': 'Flammensigal beim Brennerstart bereits vorhanden',
    'F4': 'Flammensigal nicht vorhanden',
    'F7': 'Differenzdrucksensor defekt',
    'F8': 'Brennstoffventil schliesst zu spaet',
    'F9': 'Geblaesedrehzahl beim Brennerstart zu niedrig',
    'FA': 'Geblaesestillstand nicht erreicht',
    'FD': 'Fehler Gasfeuerungsautomat',
    'FE': 'Starkes Stoerfeld (EMV) in der Naehe oder Elektronik defekt',
    'FF': 'Starkes Stoerfeld (EMV) in der Naehe oder interner Fehler'
}


systemschemes = {
    '01': 'WW',
    '02': 'HK + WW',
    '04': 'HK + WW',
    '05': 'HK + WW'
}

setreturnstatus = {
    '00': 'OK',
    '05': 'SYNC (NOT OK)',
}
