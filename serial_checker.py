#!/usr/bin/env python3
"""Kindle serial checker. Offline Python mirror of kindlemodding.github.io jailbreak wizard.

Serial -> model. Optional firmware -> matching jailbreaks. No network. Stdlib only.

Usage:
  serial_checker.py SERIAL [FIRMWARE] [--blacklisted] [--ads] [--json]

  SERIAL       full or partial serial (site asks first 8 chars; longer fine)
  FIRMWARE     e.g. 5.16.2 — adds jailbreak matching
  --blacklisted  Kindle can't register to Amazon (some jailbreaks need registration)
  --ads          lockscreen shows ads (some jailbreaks need ad-supported unit)
  --json         machine-readable output

Exit 0 on model found, 1 otherwise.
"""

import json
import re
import sys

DATA_DATE = "2026-09-25"
DATA_SOURCE = "https://github.com/KindleModding/kindlemodding.github.io"

MODELS = [{'amazon': 'Kindle (1st Generation)', 'nick': 'K1', 'nicknames': ['K1'], 'sv': 0, 'codes': {'01': ('Kindle1', 'ATVPDKIKX0DER')}, 'last_fw': '1.2.1', 'year': 2007, 'platform': 'N/A', 'board': 'Fiona', 'note': 'legacy pre-5.x device, no modern jailbreak path'}, {'amazon': 'Kindle (2nd Generation)', 'nick': 'K2', 'nicknames': ['K2'], 'sv': 0, 'codes': {'02': ('Kindle2US', 'A3UN6WX5RRO2AG'), '03': ('Kindle2International', 'A1F83G8C2ARO7P')}, 'last_fw': '2.5.8', 'year': 2009, 'platform': 'Mario/MarioDeprecated', 'board': 'Mario'}, {'amazon': 'Kindle DX (2nd Generation)', 'nick': 'DX', 'nicknames': ['DX'], 'sv': 0, 'codes': {'04': ('KindleDXUS', 'A1PA6795UKMFR9'), '05': ('KindleDXInternational', 'A13V1IB3VIYZZH'), '09': ('KindleDXGraphite', 'A3P5ROKL5A1OLE')}, 'last_fw': '2.5.8', 'year': 2009, 'platform': '???', 'board': 'Nell/NellSL/NellWW'}, {'amazon': 'Kindle Keyboard (3rd Generation)', 'nick': 'K3', 'nicknames': ['K3', 'K3G'], 'sv': 0, 'codes': {'06': ('Kindle3WiFi3G', 'A1VC38T7YXB528'), '08': ('Kindle3WiFi', 'A3AEGXETSR30VB'), '0A': ('Kindle3WiFi3GEurope', 'A3JWKAKR8XB7XF')}, 'last_fw': '3.4.3', 'year': 2010, 'platform': 'Luigi', 'board': 'Shasta'}, {'amazon': 'Kindle (4th Generation)', 'nick': 'K4', 'nicknames': ['K4', 'K4S'], 'sv': 0, 'codes': {'0E': ('Kindle4NonTouch', 'A3R76HOPU0Z2CB')}, 'last_fw': '4.1.4', 'year': 2011, 'platform': 'Yoshi', 'board': 'Tequila'}, {'amazon': 'Kindle Touch (4th Generation)', 'nick': 'KT', 'nicknames': ['KT', 'K5'], 'sv': 0, 'codes': {'0F': ('Kindle5TouchWiFi3G', 'A1IM4EOPHS76S7'), '10': ('Kindle5TouchWiFi3GEurope', 'A138L1TOL8PIJT'), '11': ('Kindle5TouchWiFi', 'A3T4TT2Z381HKD'), '12': ('Kindle5TouchUnknown', 'A3LJ5WMKNRFKQS')}, 'last_fw': '5.3.7.3', 'year': 2011, 'platform': 'Yoshi', 'board': 'Whitney'}, {'amazon': 'Kindle Paperwhite (5th Generation)', 'nick': 'PW', 'nicknames': ['PW', 'PWG'], 'sv': 0, 'codes': {'1B': ('KindlePaperWhiteWiFi3G', 'A1JYRMDPD0WRC1'), '1C': ('KindlePaperWhiteWiFi3GCanada', 'A1U5RCOVU0NYF2'), '1D': ('KindlePaperWhiteWiFi3GEurope', 'A1I7TFXKDRQDZL'), '1F': ('KindlePaperWhiteWiFi3GJapan', 'A1K21FY43GMZF8'), '20': ('KindlePaperWhiteWiFi3GBrazil', 'A3RN7G7QC5MWSZ'), '24': ('KindlePaperWhiteWiFi', 'A3VSAZHKW7EWVH')}, 'last_fw': '5.6.1.1', 'year': 2012, 'platform': 'Wario', 'board': 'Pinot'}, {'amazon': 'Kindle (5th Generation)', 'nick': 'K4', 'nicknames': ['K4', 'K4B'], 'sv': 0, 'codes': {'23': ('Kindle4NonTouchBlack', 'AMMK0LS9EDNM8')}, 'last_fw': '4.1.4', 'year': 2012, 'platform': 'Yoshi', 'board': 'Sauza'}, {'amazon': 'Kindle Paperwhite (6th Generation)', 'nick': 'PW2', 'nicknames': ['PW2', 'PW2J'], 'sv': 0, 'codes': {'5A': ('KindlePaperWhite2WiFiJapan', 'A1XFE4LQM16OSW'), 'D4': ('KindlePaperWhite2WiFi', 'A2X1JOFWQIYV75'), 'D5': ('KindlePaperWhite2WiFi3G', 'A2LTUGSV2JQ93O'), 'D6': ('KindlePaperWhite2WiFi3GCanada', 'A3CG2RMGG8NQEJ'), 'D7': ('KindlePaperWhite2WiFi3GEurope', 'A2RWEQK36M6DUE'), 'D8': ('KindlePaperWhite2WiFi3GRussia', 'A3DM9ZTSZGUSMW'), 'F2': ('KindlePaperWhite2WiFi3GJapan', 'A36L7QE2V0XKCZ'), '17': ('KindlePaperWhite2WiFi4GBInternational', 'A3I3CR3NPZFVHY'), '5F': ('KindlePaperWhite2WiFi3G4GBCanada', 'A16EMENY0O3Z2H'), '60': ('KindlePaperWhite2WiFi3G4GBEurope', 'A3D1N3J5SXSYPF'), '61': ('KindlePaperWhite2WiFi3G4GBBrazil', 'A3NRQ2KXEO33BF'), '62': ('KindlePaperWhite2WiFi3G4GB', 'A3QT0UFVNUDPAE'), 'F4': ('KindlePaperWhite2Unknown_0xF4', 'A3JI3C11GUW6OM'), 'F9': ('KindlePaperWhite2Unknown_0xF9', 'A148QFVDZ3MQ8V')}, 'last_fw': '5.12.2.2', 'year': 2013, 'platform': 'Wario', 'board': 'Pinot'}, {'amazon': 'Kindle Voyage (7th Generation)', 'nick': 'KV', 'nicknames': ['KV'], 'sv': 0, 'codes': {'13': ('KindleVoyageWiFi', 'A3FE7AD5N5R11'), '54': ('KindleVoyageWiFi3G', 'A1VHVRSIVA49BF'), '2A': ('KindleVoyageWiFi3GJapan', 'A2KSI370ME58SV'), '4F': ('KindleVoyageWiFi3G_0x4F', 'AEK24W3B90XSI'), '52': ('KindleVoyageWiFi3GMexico', 'A66ZTOXC8UWFP'), '53': ('KindleVoyageWiFi3GEurope', 'A26JMGYIXWMKGL')}, 'last_fw': '5.13.6', 'year': 2014, 'platform': 'Wario', 'board': 'Icewine'}, {'amazon': 'Kindle (7th Generation)', 'nick': 'KT2', 'nicknames': ['KT2', 'BASIC'], 'sv': 0, 'codes': {'C6': ('KindleBasic', 'A2TNPB8EVLW5FA'), 'DD': ('KindleBasicKiwi', 'A9N06WOIL49CA')}, 'last_fw': '5.12.2.2', 'year': 2014, 'platform': 'Wario', 'board': 'Bourbon'}, {'amazon': 'Kindle Paperwhite (7th Generation)', 'nick': 'PW3', 'nicknames': ['PW3'], 'sv': 1, 'codes': {'0G1': ('KindlePaperWhite3WiFi', 'A21RY355YUXQAF'), '0G2': ('KindlePaperWhite3WiFi3G', 'A6S0KGW65V1TV'), '0G4': ('KindlePaperWhite3WiFi3GMexico', 'A3P87LH4DLAKE2'), '0G5': ('KindlePaperWhite3WiFi3GEurope', 'A3OLIINW419WLP'), '0G6': ('KindlePaperWhite3WiFi3GCanada', 'AOPKCG97868D2'), '0G7': ('KindlePaperWhite3WiFi3GJapan', 'A3MTNJ7FDYZOPO'), '0KB': ('KindlePaperWhite3WhiteWiFi', 'A21RY355YUXQAF'), '0KC': ('KindlePaperWhite3WhiteWiFi3GJapan', 'A3MTNJ7FDYZOPO'), '0KD': ('KindlePW3WhiteUnknown_0KD', 'AOPKCG97868D2'), '0KE': ('KindlePaperWhite3WhiteWiFi3GInternational', 'A3OLIINW419WLP'), '0KF': ('KindlePaperWhite3WhiteWiFi3GInternationalBis', 'A6S0KGW65V1TV'), '0KG': ('KindlePW3WhiteUnknown_0KG', 'A3P87LH4DLAKE2'), '0LK': ('KindlePaperWhite3WiFi32GBJapanBlack', 'A2T9E09EBKRBWU'), '0LL': ('KindlePaperWhite3WiFi32GBJapanWhite', 'A2T9E09EBKRBWU'), 'TTT': ('KindlePW3Unknown_TTT', 'A21RY355YUXQAF')}, 'last_fw': '5.16.2.1.1', 'year': 2015, 'platform': 'Wario', 'board': 'Muscat'}, {'amazon': 'Kindle Oasis (8th Generation)', 'nick': 'KOA', 'nicknames': ['KOA'], 'sv': 1, 'codes': {'0GC': ('KindleOasisWiFi', 'A2NP90AR02CXEG'), '0GD': ('KindleOasisWiFi3G', 'A370DV3BFIHFD3'), '0GR': ('KindleOasisWiFi3GInternational', 'A21R12JDS0I7HR'), '0GS': ('KindleOasisUnknown_0GS', 'A2G9XCYZJMNLQK'), '0GT': ('KindleOasisWiFi3GChina', 'AIOUHGSC1FXK5'), '0GU': ('KindleOasisWiFi3GEurope', 'A1VYPQEAEVB479')}, 'last_fw': '5.16.2.1.1', 'year': 2016, 'platform': 'Duet', 'board': 'Whisky'}, {'amazon': 'Kindle (8th Generation)', 'nick': 'KT3', 'nicknames': ['KT3'], 'sv': 1, 'codes': {'0DU': ('KindleBasic2Unknown_0DU', None), '0K9': ('KindleBasic2', 'A363JBKK6AP29Q'), '0KA': ('KindleBasic2White', 'A363JBKK6AP29Q')}, 'last_fw': '5.16.2.1.1', 'year': 2016, 'platform': 'Heisenberg', 'board': 'Eanab'}, {'amazon': 'Kindle x Migu', 'nick': 'KM', 'nicknames': ['KM'], 'sv': 1, 'codes': {'0NG': ('UNSUPPORTED', 'UNKNOWN')}, 'last_fw': '5.7.2.8 (Based on Android 5.1.1?)', 'year': 2017, 'platform': 'Heisenberg', 'board': 'Eanab', 'note': 'runs Android, not Kindle OS — try normal Android methods'}, {'amazon': 'Kindle Oasis (9th Generation)', 'nick': 'KOA2', 'nicknames': ['KOA2'], 'sv': 1, 'codes': {'0LM': ('KindleOasis2Unknown_0LM', 'A2AVNKP6ZINL5'), '0LN': ('KindleOasis2Unknown_0LN', 'A1SZ6LXIZK7826'), '0LP': ('KindleOasis2Unknown_0LP', 'A3M646A6GS49CA'), '0LQ': ('KindleOasis2Unknown_0LQ', 'A39S6AFBERWZOH'), '0P1': ('KindleOasis2WiFi32GBChampagne', 'A1SZ6LXIZK7826'), '0P2': ('KindleOasis2Unknown_0P2', 'A2AVNKP6ZINL5'), '0P6': ('KindleOasis2Unknown_0P6', 'A3M646A6GS49CA'), '0P7': ('KindleOasis2Unknown_0P7', 'A39S6AFBERWZOH'), '0P8': ('KindleOasis2WiFi8GB', 'A1SZ6LXIZK7826'), '0S1': ('KindleOasis2WiFi3G32GB', 'A2AVNKP6ZINL5'), '0S2': ('KindleOasis2WiFi3G32GBEurope', 'A3M646A6GS49CA'), '0S3': ('KindleOasis2Unknown_0S3', 'A39S6AFBERWZOH'), '0S4': ('KindleOasis2Unknown_0S4', 'A1SZ6LXIZK7826'), '0S7': ('KindleOasis2Unknown_0S7', 'A1SZ6LXIZK7826'), '0SA': ('KindleOasis2WiFi32GB', 'A1SZ6LXIZK7826')}, 'last_fw': '5.16.2.1.1', 'year': 2017, 'platform': 'Zelda', 'board': 'Cognac'}, {'amazon': 'Kindle Paperwhite (10th Generation)', 'nick': 'PW4', 'nicknames': ['PW4'], 'sv': 1, 'codes': {'0PP': ('KindlePaperWhite4WiFi8GB', 'AJRLVDTOPT1LE'), '0T1': ('KindlePaperWhite4WiFi4G32GB', 'A3IT5K46YEJ8DG'), '0T2': ('KindlePaperWhite4WiFi4G32GBEurope', 'A2J0U8ZY7AYQWV'), '0T3': ('KindlePaperWhite4WiFi4G32GBJapan', 'AV9Q59KU8EJQE'), '0T4': ('KindlePaperWhite4Unknown_0T4', 'A27ME72Q2PS699'), '0T5': ('KindlePaperWhite4Unknown_0T5', 'A3IT5K46YEJ8DG'), '0T6': ('KindlePaperWhite4WiFi32GB', 'AJRLVDTOPT1LE'), '0T7': ('KindlePaperWhite4Unknown_0T7', 'AJRLVDTOPT1LE'), '0TJ': ('KindlePaperWhite4Unknown_0TJ', 'AJRLVDTOPT1LE'), '0TK': ('KindlePaperWhite4Unknown_0TK', 'AJRLVDTOPT1LE'), '0TL': ('KindlePaperWhite4Unknown_0TL', 'A2J0U8ZY7AYQWV'), '0TM': ('KindlePaperWhite4Unknown_0TM', 'AV9Q59KU8EJQE'), '0TN': ('KindlePaperWhite4Unknown_0TN', 'A27ME72Q2PS699'), '102': ('KindlePaperWhite4WiFi8GBIndia', 'AJRLVDTOPT1LE'), '103': ('KindlePaperWhite4WiFi32GBIndia', 'A2J0U8ZY7AYQWV'), '16Q': ('KindlePaperWhite4WiFi32GBBlue', 'AJRLVDTOPT1LE'), '16R': ('KindlePaperWhite4WiFi32GBPlum', 'AJRLVDTOPT1LE'), '16S': ('KindlePaperWhite4WiFi32GBSage', 'AJRLVDTOPT1LE'), '16T': ('KindlePaperWhite4WiFi8GBBlue', 'AJRLVDTOPT1LE'), '16U': ('KindlePaperWhite4WiFi8GBPlum', 'AJRLVDTOPT1LE'), '16V': ('KindlePaperWhite4WiFi8GBSage', 'AJRLVDTOPT1LE'), '0PL': ('KindlePW4Unknown_0PL', 'A3IT5K46YEJ8DG')}, 'last_fw': 'Not Yet Discontinued', 'year': 2018, 'platform': 'Rex', 'board': 'Jaeger'}, {'amazon': 'Kindle (10th Generation)', 'nick': 'KT4', 'nicknames': ['KT4'], 'sv': 1, 'codes': {'10L': ('KindleBasic3', 'AHU5VU98ZZYIL'), '0WF': ('KindleBasic3White8GB', 'AHU5VU98ZZYIL'), '0WG': ('KindleBasic3Unknown_0WG', 'AHU5VU98ZZYIL'), '0WH': ('KindleBasic3White', 'AHU5VU98ZZYIL'), '0WJ': ('KindleBasic3Unknown_0WJ', 'AHU5VU98ZZYIL'), '0VB': ('KindleBasic3KidsEdition', 'AHU5VU98ZZYIL')}, 'last_fw': 'Not Yet Discontinued', 'year': 2019, 'platform': 'Rex', 'board': 'Moonshine'}, {'amazon': 'Kindle Oasis (10th Generation)', 'nick': 'KOA3', 'nicknames': ['KOA3', 'KOA3W32C'], 'sv': 1, 'codes': {'11L': ('KindleOasis3WiFi32GBChampagne', 'A2NW3VDYR5P8Z0'), '0WQ': ('KindleOasis3WiFi4G32GBJapan', 'A28MDQJEP7D12S'), '0WP': ('KindleOasis3WiFi4G32GBIndia', 'A2M7UZTFTYKRHM'), '0WN': ('KindleOasis3WiFi4G32GB', 'AB6KN53ZYVL6D'), '0WM': ('KindleOasis3WiFi32GB', 'A2NW3VDYR5P8Z0'), '0WL': ('KindleOasis3WiFi8GB', 'A2NW3VDYR5P8Z0')}, 'last_fw': '5.18.2', 'year': 2019, 'platform': 'Zelda', 'board': 'Stinger'}, {'amazon': 'Kindle Paperwhite (11th Generation)', 'nick': 'PW5', 'nicknames': ['PW5', 'PW5SE'], 'sv': 1, 'codes': {'1LG': ('KindlePaperWhite5SignatureEdition', 'A328XUBPG464LQ'), '1Q0': ('KindlePaperWhite5Unknown_1Q0', 'A328XUBPG464LQ'), '1PX': ('KindlePaperWhite5', 'A328XUBPG464LQ'), '1VD': ('KindlePaperWhite5Unknown_1VD', 'A328XUBPG464LQ'), '219': ('KindlePaperWhite5SE_219', 'A328XUBPG464LQ'), '21A': ('KindlePaperWhite5_21A', 'A328XUBPG464LQ'), '2BH': ('KindlePaperWhite5SE_2BH', 'A328XUBPG464LQ'), '2BJ': ('KindlePaperWhite5Unknown_2BJ', 'A328XUBPG464LQ'), '2DK': ('KindlePaperWhite5_2DK', 'A328XUBPG464LQ')}, 'last_fw': 'Not Yet Discontinued', 'year': 2021, 'platform': 'Bellatrix', 'board': 'Malbec'}, {'amazon': 'Kindle (11th Generation) - 2022 Release', 'nick': 'KT5', 'nicknames': ['KT5'], 'sv': 1, 'codes': {'22D': ('KindleBasic4Unknown_22D', 'A1S35GJCTB6VUN'), '25T': ('KindleBasic4Unknown_25T', 'A1S35GJCTB6VUN'), '23A': ('KindleBasic4Unknown_23A', 'A1S35GJCTB6VUN'), '2AQ': ('KindleBasic4_2AQ', 'A1S35GJCTB6VUN'), '2AP': ('KindleBasic4_2AP', 'A1S35GJCTB6VUN'), '1XH': ('KindleBasic4Unknown_1XH', 'A1S35GJCTB6VUN'), '22C': ('KindleBasic4Unknown_22C', 'A1S35GJCTB6VUN')}, 'last_fw': 'Not Yet Discontinued', 'year': 2022, 'platform': 'Bellatrix', 'board': 'Cava'}, {'amazon': 'Kindle Scribe - 2022 Release', 'nick': 'KS', 'nicknames': ['KS'], 'sv': 1, 'codes': {'27J': ('KindleScribeUnknown_27J', 'A12KI9K1KHHBVF'), '2BL': ('KindleScribeUnknown_2BL', 'A12KI9K1KHHBVF'), '263': ('KindleScribeUnknown_263', 'A12KI9K1KHHBVF'), '227': ('KindleScribe16GB_227', 'A12KI9K1KHHBVF'), '2BM': ('KindleScribeUnknown_2BM', 'A12KI9K1KHHBVF'), '23L': ('KindleScribe_23L', 'A12KI9K1KHHBVF'), '23M': ('KindleScribe64GB_23M', 'A12KI9K1KHHBVF'), '270': ('KindleScribeUnknown_270', 'A12KI9K1KHHBVF')}, 'last_fw': 'Not Yet Discontinued', 'year': 2022, 'platform': 'Bellatrix3', 'board': 'Barolo'}, {'amazon': 'Kindle (11th Generation) - 2024 Release', 'nick': 'KT6', 'nicknames': ['KT6'], 'sv': 1, 'codes': {'3L5': ('KindleBasic5Unknown_3L5', 'A2AJ1N357FEMTV'), '3L6': ('KindleBasic5Unknown_3L6', 'A2AJ1N357FEMTV'), '3L4': ('KindleBasic5Unknown_3L4', 'A2AJ1N357FEMTV'), '3L3': ('KindleBasic5Unknown_3L3', 'A2AJ1N357FEMTV'), 'A89': ('KindleBasic5Unknown_A89', 'A2AJ1N357FEMTV'), '3L2': ('KindleBasic5Unknown_3L2', 'A2AJ1N357FEMTV'), '3KM': ('KindleBasic5Unknown_3KM', 'A2AJ1N357FEMTV')}, 'last_fw': 'Not Yet Discontinued', 'year': 2024, 'platform': 'Bellatrix', 'board': 'Rossini'}, {'amazon': 'Kindle Paperwhite (12th Generation) - 2024 Release', 'nick': 'PW6', 'nicknames': ['PW6'], 'sv': 1, 'codes': {'349': ('KindlePaperWhite6Unknown_349', 'A1BF5SA90HOYO2'), '346': ('KindlePaperWhite6Unknown_346', 'A1BF5SA90HOYO2'), '33X': ('KindlePaperWhite6Unknown_33X', 'A1BF5SA90HOYO2'), '33W': ('KindlePaperWhite6Unknown_33W', 'A1BF5SA90HOYO2'), '3HA': ('KindlePaperWhite6Unknown_3HA', 'A1BF5SA90HOYO2'), '3H5': ('KindlePaperWhite6Unknown_3H5', 'A1BF5SA90HOYO2'), '3H3': ('KindlePaperWhite6Unknown_3H3', 'A1BF5SA90HOYO2'), '3H8': ('KindlePaperWhite6Unknown_3H8', 'A1BF5SA90HOYO2'), '3J5': ('KindlePaperWhite6Unknown_3J5', 'A1BF5SA90HOYO2'), '3JS': ('KindlePaperWhite6Unknown_3JS', 'A1BF5SA90HOYO2')}, 'last_fw': 'Not Yet Discontinued', 'year': 2024, 'platform': 'Bellatrix4', 'board': 'Sangria'}, {'amazon': 'Kindle Scribe - 2024 Release', 'nick': 'KS2', 'nicknames': ['KS2'], 'sv': 1, 'codes': {'3V0': ('KindleScribe2Unknown_3V0', 'A3TY6T3X94EBV6'), '3V1': ('KindleScribe2Unknown_3V1', 'A3TY6T3X94EBV6'), '3X5': ('KindleScribe2Unknown_3X5', 'A3TY6T3X94EBV6'), '3UV': ('KindleScribe2Unknown_3UV', 'A3TY6T3X94EBV6'), '3X4': ('KindleScribe2Unknown_3X4', 'A3TY6T3X94EBV6'), '3X3': ('KindleScribe2Unknown_3X3', 'A3TY6T3X94EBV6'), '41E': ('KindleScribe2Unknown_41E', 'A3TY6T3X94EBV6'), '41D': ('KindleScribe2Unknown_41D', 'A3TY6T3X94EBV6')}, 'last_fw': 'Not Yet Discontinued', 'year': 2024, 'platform': 'Bellatrix3', 'board': 'Pisco'}, {'amazon': 'Kindle Colorsoft (1st Generation)', 'nick': 'CS', 'nicknames': ['CS'], 'sv': 1, 'codes': {'3H9': ('KindleColorSoftUnknown_3H9', 'A2CU9ZQDNZFID4'), '3H4': ('KindleColorSoftUnknown_3H4', 'A2CU9ZQDNZFID4'), '3HB': ('KindleColorSoftUnknown_3HB', 'A2CU9ZQDNZFID4'), '3H6': ('KindleColorSoftUnknown_3H6', 'A2CU9ZQDNZFID4'), '3H2': ('KindleColorSoftUnknown_3H2', 'A2CU9ZQDNZFID4'), '34X': ('KindleColorSoftUnknown_34X', 'A2CU9ZQDNZFID4'), '3H7': ('KindleColorSoftUnknown_3H7', 'A2CU9ZQDNZFID4'), '3JT': ('KindleColorSoftUnknown_3JT', 'A2CU9ZQDNZFID4'), '3J6': ('KindleColorSoftUnknown_3J6', 'A2CU9ZQDNZFID4'), '456': ('KindleColorSoftUnknown_456', 'A2CU9ZQDNZFID4'), '455': ('KindleColorSoftUnknown_455', 'A2CU9ZQDNZFID4'), '4EP': ('KindleColorSoftUnknown_4EP', 'A2CU9ZQDNZFID4')}, 'last_fw': 'Not Yet Discontinued', 'year': 2024, 'platform': 'Bellatrix4', 'board': 'Seabreeze'}, {'amazon': 'Kindle Scribe (3rd Generation)', 'nick': 'KS3', 'nicknames': ['KS3'], 'sv': 1, 'codes': {'4PG': ('KindleScribe3Unknown_4PG', 'A2PZKJK345L1G8'), '4PE': ('KindleScribe3Unknown_4PE', 'A2PZKJK345L1G8'), '4PL': ('KindleScribe3Unknown_4PL', 'AC66OWFZXI53A'), '4F8': ('KindleScribe3Unknown_4F8', 'A2PZKJK345L1G8'), '4FA': ('KindleScribe3Unknown_4FA', 'A2PZKJK345L1G8'), '454': ('KindleScribe3Unknown_454', 'A2PZKJK345L1G8')}, 'last_fw': 'Not Yet Discontinued', 'year': 2025, 'platform': 'Platpa6', 'board': 'Paloma', 'note': 'no jailbreak released yet'}, {'amazon': 'Kindle Scribe Colorsoft (1st Generation)', 'nick': 'KSC', 'nicknames': ['KSC'], 'sv': 1, 'codes': {'4VX': ('KindleScribeColorSoftUnknown_4VX', 'A3PXY43G91LWNT'), '4PF': ('KindleScribeColorSoftUnknown_4PF', 'A3PXY43G91LWNT'), '4PH': ('KindleScribeColorSoftUnknown_4PH', 'A3PXY43G91LWNT'), '4F9': ('KindleScribeColorSoftUnknown_4F9', 'A3PXY43G91LWNT'), '4FB': ('KindleScribeColorSoftUnknown_4FB', 'A3PXY43G91LWNT'), '46P': ('KindleScribeColorSoftUnknown_46P', 'A3PXY43G91LWNT')}, 'last_fw': 'Not Yet Discontinued', 'year': 2025, 'platform': 'Platcs8', 'board': 'Calvados', 'note': 'no jailbreak released yet'}]

JAILBREAKS = [{'name': 'WinterBreak2', 'url': '/jailbreaking/WinterBreak2/', 'registration': False, 'ads': False, 'models': ['PW', 'PW2', 'KV', 'KT2', 'PW3', 'KOA', 'KT3', 'KOA2', 'PW4', 'KT4', 'KOA3', 'PW5', 'KT5', 'KS'], 'firmwares': [{'models': ['all'], 'min': '5.6.1.1', 'max': '5.16.3', 'accepted': ['5.16.5'], 'denied': []}]}, {'name': 'SpiderCat', 'url': '/jailbreaking/SpiderCat', 'registration': False, 'ads': False, 'models': ['PW4', 'KT4', 'KOA3', 'PW5', 'KT5', 'KT6', 'PW6', 'CS', 'KS', 'KS2'], 'firmwares': [{'models': ['all'], 'min': '5.16.3', 'max': '5.19.5', 'accepted': [], 'denied': []}]}, {'name': 'Véra', 'url': '/jailbreaking/Vera', 'registration': False, 'ads': False, 'models': ['PW5', 'KT5', 'KT6', 'PW6', 'CS', 'KS', 'KS2'], 'firmwares': [{'models': ['all'], 'min': '5.17.1', 'max': '5.19.6', 'accepted': [], 'denied': []}]}, {'name': 'Nosebleed', 'url': '/jailbreaking/Nosebleed/', 'registration': False, 'ads': False, 'models': ['KT5', 'PW5', 'KOA3', 'PW6', 'KT6'], 'firmwares': [{'models': ['KT5', 'PW5', 'KOA3'], 'min': '5.16.4', 'max': '5.18.6', 'accepted': [], 'denied': []}, {'models': ['PW6', 'KT6'], 'min': '5.16.4', 'max': '5.17.1.0.4', 'accepted': [], 'denied': []}]}, {'name': 'Sanctuary', 'url': '/jailbreaking/Sanctuary', 'registration': False, 'ads': False, 'models': ['PW4', 'KT4', 'KOA3', 'PW5', 'KT5', 'KS', 'KT6', 'PW6', 'KS2', 'CS'], 'firmwares': [{'models': ['all'], 'min': '5.16.4', 'max': '5.18.3', 'accepted': [], 'denied': ['5.16.5']}]}, {'name': 'WinterBreak', 'url': '/jailbreaking/WinterBreak/', 'registration': True, 'ads': False, 'models': ['PW', 'PW2', 'KV', 'KT2', 'PW3', 'KOA', 'KT3', 'KOA2', 'PW4', 'KT4', 'KOA3', 'PW5', 'KT5', 'KS', 'KT6', 'PW6', 'KS2', 'CS'], 'firmwares': [{'models': ['all'], 'min': '5.6.1.1', 'max': '5.18.0.2', 'accepted': [], 'denied': []}]}, {'name': 'SpringBreak', 'url': '/jailbreaking/SpringBreak', 'registration': True, 'ads': False, 'models': ['KT5', 'PW5', 'KT4', 'PW4'], 'firmwares': [{'models': ['KT5', 'PW5'], 'min': '5.18.1', 'max': '5.19.2.0.1', 'accepted': [], 'denied': []}, {'models': ['KT4', 'PW4'], 'min': '5.18.1', 'max': '5.18.1.1.1', 'accepted': [], 'denied': []}]}, {'name': 'AdBreak', 'url': '/jailbreaking/AdBreak/', 'registration': True, 'ads': True, 'models': ['PW4', 'KT4', 'KOA3', 'PW5', 'KT5', 'KS', 'KT6', 'PW6'], 'firmwares': [{'models': ['KOA3', 'PW5', 'KT5', 'KS', 'KT6', 'PW6'], 'min': '5.18.1', 'max': '5.18.5.0.1', 'accepted': [], 'denied': []}, {'models': ['PW4', 'KT4'], 'min': '5.18.1', 'max': '5.18.1', 'accepted': [], 'denied': []}]}, {'name': 'NiLuJe K2/DX/DXG/K3 Jailbreak', 'url': '/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/', 'registration': False, 'ads': False, 'models': ['K2', 'DX', 'K3'], 'firmwares': [{'models': ['all'], 'min': '2.0.0', 'max': '4.0.0', 'accepted': [], 'denied': []}]}, {'name': 'NiLuJe K4 Jailbreak', 'url': '/jailbreaking/Legacy/K4-Jailbreak/', 'registration': False, 'ads': False, 'models': ['K4'], 'firmwares': [{'models': ['all'], 'min': '2.0.0', 'max': '5.0.0', 'accepted': [], 'denied': []}]}, {'name': 'NiLuJe K5 Jailbreak', 'url': '/jailbreaking/Legacy/K5-Jailbreak/', 'registration': False, 'ads': False, 'models': ['KT'], 'firmwares': [{'models': ['all'], 'min': '5.0.0', 'max': '5.4.4.2', 'accepted': [], 'denied': []}]}, {'name': 'LEGACY', 'url': '/jailbreaking/Legacy/index.html', 'registration': False, 'ads': False, 'models': ['K1'], 'firmwares': [{'models': ['all'], 'min': '0.0.0', 'max': '2.0.0', 'accepted': [], 'denied': []}]}, {'name': 'Android Jailbreak Methods', 'url': 'https://www.mobileread.com/forums/showthread.php?p=4087697', 'registration': False, 'ads': False, 'models': ['KM'], 'firmwares': [{'models': ['all'], 'min': '0.0.0', 'max': '999.0.0', 'accepted': [], 'denied': []}]}]

HEX = frozenset("0123456789ABCDEF")


def get_serial_info(serial):
    # port of getSerialInfo() in jailbreakFinder.js
    n = len(serial)
    if n == 2 or n == 3:
        return {"serial_version": 0 if n == 2 else 1, "device_code": serial}
    if serial[0] == "G":
        if n < 6:
            return -1
        return {"serial_version": 1, "device_code": serial[3:6]}
    if serial[0] in HEX:
        if n < 4:
            return -1
        return {"serial_version": 0, "device_code": serial[2:4]}
    return -2


def find_model(serial):
    # port of searchForSerial()
    s = serial.upper().replace(" ", "")
    if not s:
        return {"ok": False, "error": "empty"}
    info = get_serial_info(s)
    if info == -1:
        return {"ok": False, "error": "too_short", "serial": s}
    if info == -2:
        return {"ok": False, "error": "invalid", "serial": s}
    for m in MODELS:
        if m["sv"] < info["serial_version"]:
            continue
        variant = m["codes"].get(info["device_code"])
        if variant is not None:
            return {
                "ok": True,
                "serial": s,
                "device_code": info["device_code"],
                "serial_version": info["serial_version"],
                "model": m,
                "variant": {"kindletool_name": variant[0], "amazon_model_id": variant[1]},
            }
    return {"ok": False, "error": "not_found", "serial": s,
            "device_code": info["device_code"]}


def cmp_ver(a, b):
    # port of versions(): numeric compare, zero-padded
    pa = [int(x) for x in a.split(".")]
    pb = [int(x) for x in b.split(".")]
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa))
    pb += [0] * (n - len(pb))
    for x, y in zip(pa, pb):
        if x != y:
            return 1 if x > y else -1
    return 0


FW_RE = re.compile(r"^\d{1,2}(\.\d{1,2}){1,5}$")


def clean_firmware(fw):
    # port of validateFirmware(): strip junk, X.XX.[...] format, major <= 5
    fw = re.sub(r"[^0-9.]", "", fw)
    if FW_RE.match(fw) and int(fw.split(".")[0]) <= 5:
        return fw
    return None


def find_jailbreaks(nick, firmware, blacklisted=False, ads=False):
    # port of fillResults()
    out = []
    for jb in JAILBREAKS:
        if nick not in jb["models"]:
            continue
        if jb["registration"] and blacklisted:
            continue
        if jb["ads"] and not ads:
            continue
        for rule in jb["firmwares"]:
            if "all" not in rule["models"] and nick not in rule["models"]:
                continue
            if firmware in rule["denied"]:
                continue
            if firmware in rule["accepted"] or (
                cmp_ver(firmware, rule["min"]) >= 0
                and cmp_ver(firmware, rule["max"]) <= 0
            ):
                out.append(jb)
                break
    return out


def screen(serial, firmware=None, blacklisted=False, ads=False):
    r = find_model(serial)
    if not r.get("ok") or firmware is None:
        return r
    fw = clean_firmware(firmware)
    if fw is None:
        r["firmware_error"] = "bad_format"
        return r
    r["firmware"] = fw
    r["jailbreaks"] = [
        {"name": j["name"], "url": "https://kindlemodding.github.io" + j["url"]}
        for j in find_jailbreaks(r["model"]["nick"], fw, blacklisted, ads)
    ]
    return r


def _human(r):
    if not r.get("ok"):
        err = r.get("error", "?")
        hint = {
            "empty": "give it a serial",
            "too_short": "serial too short (need 2+ chars; G-serials need 6+)",
            "invalid": "must start with G (new) or 0-9/A-F (old)",
            "not_found": "code %s unknown — open issue on kindlemodding.github.io" % r.get("device_code", "?"),
        }.get(err, err)
        return "no match: %s" % hint
    m = r["model"]
    v = r["variant"]
    lines = [
        "model: %s [%s]" % (m["amazon"], m["nick"]),
        "variant: %s (%s)" % (v["kindletool_name"], v["amazon_model_id"] or "?"),
        "released %s, %s / %s, last fw: %s" % (m["year"], m["platform"], m["board"], m["last_fw"]),
    ]
    if m.get("note"):
        lines.append("note: %s" % m["note"])
    if "firmware_error" in r:
        lines.append("firmware ignored: bad format (want X.XX[.XX...], major <= 5)")
    elif "firmware" in r:
        jbs = r["jailbreaks"]
        lines.append("firmware %s -> %s" % (
            r["firmware"],
            ", ".join(j["name"] for j in jbs) if jbs else "no jailbreak available",
        ))
    return "\n".join(lines)


def main(argv):
    flags = {a for a in argv if a.startswith("-")}
    args = [a for a in argv if not a.startswith("-")]
    if not args or "-h" in flags or "--help" in flags:
        print(__doc__.strip())
        return 2
    r = screen(
        args[0],
        args[1] if len(args) > 1 else None,
        "--blacklisted" in flags,
        "--ads" in flags,
    )
    if "--json" in flags:
        print(json.dumps(r, indent=2))
    else:
        print(_human(r))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
