import argparse
import pandas as pd
import sys
import requests
import re

def remove_accents(string):
    if type(string) is not str:
        string = str(string, encoding='utf-8')

    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[èéêë]", 'e', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[ýÿ]", 'y', string)

    return string

def find_circo(dataframe, departement, circonscription):
    is_dep =  dataframe['département'] == departement
    dataframe_dep = dataframe[is_dep]
    is_circo =  dataframe_dep['circonscription'] == circonscription
    dataframe_circo = dataframe_dep[is_circo]
    return dataframe_circo

def premier_tour(dataframe):
    print("| inscrits = ", int(dataframe['Inscrits']), sep = '')
    print("| votants = ", int(dataframe['Votants']), sep = '')
    print("| exprimes = ", int(dataframe['Exprimés']), sep = '')

def exist_second(dataframe):
    dicocirc = dataframe.to_dict(orient='list')
    if str(dicocirc['élu premier tour'][0]) == 'O':
        monotour = True
        print("{{Résultats électoraux|candidats")
    else:
        monotour = False
        print("{{Résultats électoraux|2tours")
    return monotour

def exist_second_post(dataframe):
    if dataframe.empty == True:
        monotour = True
        print("{{Résultats électoraux|candidats")
    else:
        monotour = False
        print("{{Résultats électoraux|2tours")
    return monotour

def corps(premier_tour, second_tour, tour, dataframe_second):
    dicocirc = premier_tour.to_dict(orient='list')
    if tour is False:
        for k, v, in second_tour.items():
            if k in dicocirc:
                if k == 'RIUDR':
                    if 'RI' in dicocirc.keys() and dicocirc['RI'][0] > 0:
                        dicocirc['RI'].append(int(v))
                    elif 'UDR' in dicocirc.keys() and dicocirc['UDR'][0] > 0:
                        dicocirc['UDR'].append(int(v))
                    else:
                        dicocirc[k].append(int(v))
                else:
                    dicocirc[k].append(int(v))
        print("| inscrits2 = ", int(dataframe_second['Inscrits']), sep = '')
        print("| votants2 = ", int(dataframe_second['Votants']), sep = '')
        print("| exprimes2 = ", int(dataframe_second['Exprimés']), sep = '')
        i = 1
        for k, v in sorted(dicocirc.items(), key=lambda x: x[1], reverse=True):
            if v != [0, 0] and v != [0]:
                print("| candidat", i," = Inconnu", sep = '')
                partie_name(k, i)
                print("| suffrages", i, " = ", v[0], sep = '')
                if v[1] == 0:
                    pass
                else:
                    print("| suffrages", i, "b = ", v[1], sep = '')
                couleur_hex(k, i)
                i += 1
        print("}}")
    else:
        i = 1
        for k, v in sorted(dicocirc.items(), key=lambda x: x[1], reverse=True):
            if v != [0, 0] and v != [0]:
                print("| candidat", i," = Inconnu", sep = '')
                partie_name(k, i)
                print("| suffrages", i, " = ", v[0], sep = '')
                couleur_hex(k, i)
                i += 1
        print("}}")

def corps_post(premier_tour, second_tour, tour, wikidata_name):
    #construction des dictionnaires
    dicocirc_premier = premier_tour.to_dict(orient='list')
    dicocirc_second = second_tour.to_dict(orient='list')
    #construction des dictionnaire detailler
    diconom = {}
    dicovoix = {}
    dicolabel = {}
    u = 1
    check = 'BEGIN'
    nuance = str(u) + ' nuance'
    #tant qu il existe un candidat
    while type(check) != float:
        prenom = str(u) + ' Prénom candidat'
        nom = str(u) + ' Nom candidat'
        voix = str(u) + ' voix'
        label = str(u) + ' Etiquette liste'
        another_lab = dicocirc_premier[nuance][0] + dicocirc_premier[nom][0]
        #recupere le nom
        diconom[another_lab] = [dicocirc_premier[prenom][0].title(), dicocirc_premier[nom][0].title()]
        #recupere les voix
        dicovoix[another_lab] = [int(dicocirc_premier[voix][0])]
        if type(dicocirc_premier[label][0]) == float:
            dicolabel[another_lab] = 'empty'
        else:
            dicolabel[another_lab] = dicocirc_premier[label][0].title()
        #verifie l existence d'un candidat supplementaire
        u += 1
        nuance = str(u) + ' nuance'
        if nuance in dicocirc_premier:
            #verifie l existence d'un candidat supplementaire
            check = dicocirc_premier[nuance][0]
        else:
            check = 0.5

    # si election a 2 tours
    if tour is False:
        i = 1
        check = 'BEGIN'
        nuance = str(i) + ' nuance'
        while type(check) != float and i < 4:
            voix = str(i) + ' voix'
            nom = str(i) + ' Nom candidat'
            another_lab = dicocirc_second[nuance][0] + dicocirc_second[nom][0]
            dicovoix[another_lab].append(int(dicocirc_second[voix][0]))
            i += 1
            nuance = str(i) + ' nuance'
            if nuance in dicocirc_second:
                check = dicocirc_second[nuance][0]
            else:
                check = float()

        print("| inscrits2 = ", int(second_tour['Inscrits']), sep = '')
        print("| votants2 = ", int(second_tour['Votants']), sep = '')
        print("| exprimes2 = ", int(second_tour['Exprimés']), sep = '')
        i = 1
        for k, v in sorted(dicovoix.items(), key=lambda x: x[1], reverse=True):
            # verifier si elue possede une page wikipedia
            if diconom[k][0] + " " + diconom[k][1] in wikidata_name.keys():
                #si le nom de page different
                if diconom[k][0] + " " + diconom[k][1] != wikidata_name[diconom[k][0] + " " + diconom[k][1]]:
                    #si le nom de page different
                    if diconom[k][0] + " " + diconom[k][1] != remove_accents(wikidata_name[diconom[k][0] + " " + diconom[k][1]]):
                        print("| candidat", i, " = [[", wikidata_name[diconom[k][0] + " " + diconom[k][1]], "|", diconom[k][0], " ", diconom[k][1], "]]", sep = '')
                    #si probleme d'accent
                    else:
                        print("| candidat", i, " = [[", wikidata_name [diconom[k][0] + " " + diconom[k][1]], "]]", sep = '')
                #si probleme d'accent
                else:
                    print("| candidat", i, " = [[", diconom[k][0], " ", diconom[k][1], "]]", sep = '')
            #si il ne possede pas de page wikipedia
            else:
                print("| candidat", i, " = ", diconom[k][0], " ", diconom[k][1], sep = '')
            partie_name_post(k, i, dicolabel)
            #affichage du suffrage
            print("| suffrages", i, " = ", dicovoix[k][0], sep = '')
            #si elue present au second tours
            if len(dicovoix[k]) == 2:
                print("| suffrages", i, "b = ", dicovoix[k][1], sep = '')
            else:
                pass
            couleur_hex_post(k, i, dicolabel)
            i += 1
        print("}}")
    # si election monotour
    else:
        i = 1
        # pour chaque voix dans l'ordre
        for k, v in sorted(dicovoix.items(), key=lambda x: x[1], reverse=True):
            # verifier si elue possede une page wikipedia
            if diconom[k][0] + " " + diconom[k][1] in wikidata_name.keys():
                #si le nom de page different
                if diconom[k][0] + " " + diconom[k][1] != wikidata_name[diconom[k][0] + " " + diconom[k][1]]:
                    #si le nom de page different
                    if diconom[k][0] + " " + diconom[k][1] != remove_accents(wikidata_name[diconom[k][0] + " " + diconom[k][1]]):
                        print("| candidat", i, " = [[", wikidata_name[diconom[k][0] + " " + diconom[k][1]], "|", diconom[k][0], " ", diconom[k][1], "]]", sep = '')
                    #si probleme d'accent
                    else:
                        print("| candidat", i, " = [[", wikidata_name [diconom[k][0] + " " + diconom[k][1]], "]]", sep = '')
                #si probleme d'accent
                else:
                    print("| candidat", i, " = [[", diconom[k][0], " ", diconom[k][1], "]]", sep = '')
            #si il ne possede pas de page wikipedia
            else:
                print("| candidat", i, " = ", diconom[k][0], " ", diconom[k][1], sep = '')
            partie_name_post(k, i, dicolabel)
            print("| suffrages", i, " = ", dicovoix[k][0], sep = '')
            couleur_hex_post(k, i, dicolabel)
            i += 1
        print("}}")

def switch_departement(argument):
    switcher = {
        'AISNE': "de l'",
        'ALLIER': "de l'",
        'ALPES-DE-HAUTE-PROVENCE': "des ",
        'HAUTES-ALPES': "des ",
        'ALPES-MARITIMES': "des ",
        'ARDÈCHE': "de l'",
        'ARDENNES': "des ",
        'ARIÈGE': "de l'",
        'AUBE': "de l'",
        'AUDE': "de l'",
        'AVEYRON': "de l'",
        'BOUCHES-DU-RHÔNE': "des ",
        'CALVADOS': "du ",
        'CANTAL': "des ",
        'CHARENTE': "de la ",
        'CHARENTE-MARITIME': "de la ",
        'CHER': "du ",
        'CORRÈZE': "de la ",
        'CORSE-DU-SUD': "de la ",
        'HAUTE-CORSE': "de la ",
        "CÔTE-D'OR": "de la ",
        "CÔTES-D'ARMOR": "de la ",
        'CREUSE': "de la ",
        'DORDOGNE': "de la ",
        'DOUBS': "du ",
        'DRÔME': "de la ",
        'EURE': "de l'",
        'EURE-ET-LOIR': "de l'",
        'FINISTÈRE': "du ",
        'GARD': "du ",
        'HAUTE-GARONNE': "de la ",
        'GERS': "du ",
        'GIRONDE': "de la ",
        'HÉRAULT': "de l'",
        'ILLE-ET-VILAINE': "de l'",
        'INDRE': "de l'",
        'INDRE-ET-LOIRE': "de l'",
        'ISÈRE': "de l'",
        'JURA': "du ",
        'LANDES': "des ",
        'LOIR-ET-CHER': "du ",
        'LOIRE': "de la ",
        'HAUTE-LOIRE': "de la ",
        'LOIRE-ATLANTIQUE': "de la ",
        'LOIRET': "du ",
        'LOT': "du ",
        'LOT-ET-GARONNE': "du ",
        'LOZÈRE': "de la ",
        'MAINE-ET-LOIRE': "de la ",
        'MANCHE': "de la ",
        'MARNE': "de la ",
        'HAUTE-MARNE': "de la ",
        'MAYENNE': "de la ",
        'MEURTHE-ET-MOSELLE': "de la ",
        'MEUSE': "de la ",
        'MORBIHAN': "du ",
        'MOSELLE': "de la ",
        'NIÈVRE': "de la ",
        'NORD': "du ",
        'OISE': "de l'",
        'ORNE': "de l'",
        'PAS-DE-CALAIS': "du ",
        'PUY-DE-DÔME': "du ",
        'PYRÉNÉES-ATLANTIQUES': "des ",
        'HAUTES-PYRÉNÉES': "des ",
        'PYRÉNÉES-ORIENTALES': "des ",
        'BAS-RHIN': "du ",
        'HAUT-RHIN': "du ",
        'RHONE': "de la ",
        'HAUTE-SAÔNE': "de la ",
        'SAÔNE-ET-LOIRE': "de la ",
        'SAONE-ET-LOIRE': "de la ",
        'SARTHE': "de la ",
        'SAVOIE': "de la ",
        'HAUTE-SAVOIE': "de la ",
        'PARIS': "de ",
        'SEINE-MARITIME': "de la ",
        'SEINE-ET-MARNE': "de la ",
        'YVELINES': "des ",
        'DEUX-SÈVRES': "des ",
        'SOMME': "de la ",
        'TARN': "de la ",
        'TARN-ET-GARONNE': "de la ",
        'VAR': "de la ",
        'VAUCLUSE': "de la ",
        'VENDÉE': "de la ",
        'VIENNE': "de la ",
        'HAUTE-VIENNE': "de la ",
        'VOSGES': "des ",
        'YONNE': "de l'",
        'TERRITOIRE DE BELFORT': "du ",
        'ESSONNE': "de l'",
        'HAUTS-DE-SEINE': "des ",
        'SEINE-SAINT-DENIS': "de la ",
        'VAL-DE-MARNE': "du ",
        "VAL-D'OISE": "du ",
        'GUADELOUPE': "de la ",
        'MARTINIQUE': "de la ",
        'GUYANE': "de la ",
        'LA RÉUNION': "de la ",
        'MAYOTTE': "de ",
    }
    return switcher.get(argument, "ERROR")

def election(annee, jour, date, departement, cironscription):
    if annee == 2012:
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
    else:
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xls', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xls', index_col=None)

    first_tour_circo = find_circo(first_tour, departement, cironscription)
    second_tour_circo = find_circo(second_tour, departement, cironscription)

    if first_tour_circo.empty:
        pass
    else:
        print("=== Élections de ", annee, " ===", sep = '')
        if annee >= 1981:
            monotour = exist_second_post(second_tour_circo)
        else:
            monotour = exist_second(second_tour_circo)
        print("| titre = Résultats des élections législatives des ", jour, " ", annee, " de la ", param.circo, "e circonscription ", switch_departement(param.departement), param.departement.title(), sep = '')
        print("| references = <ref>Résultats des élections législatives françaises premier tour du ", date, " par circonscription, cdsp_legi", annee, "t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>", sep = '')

        premier_tour(first_tour_circo)
        if annee >= 1988:
            corps_post(first_tour_circo, second_tour_circo, monotour, candidat_list)
        else:
            subseta = first_tour_circo.iloc[:,7:first_tour_circo.size]
            subsetb = second_tour_circo.iloc[:,8:second_tour_circo.size]
            corps(subseta, subsetb, monotour, second_tour_circo)
        print("\n")

def couleur_hex(argument, order_number):
    switcher = {
        'COM': " = {{Infobox Parti politique français/couleurs|-PCF}}",
        'COM2': " = {{Infobox Parti politique français/couleurs|-COM}}",
        'UFD': " = {{Infobox Parti politique français/couleurs|-UFD}}",
        'SFIO': " = {{Infobox Parti politique français/couleurs|-SFIO}}",
        'RADSOC': " = {{Infobox Parti politique français/couleurs|-DVG}}",
        'RADICAUX GAUCHE': " = {{Infobox Parti politique français/couleurs|-DVG}}",
        'RADCENT': " = {{Infobox Parti politique français/couleurs|-DVG}}",
        'RADUFD': " = {{Infobox Parti politique français/couleurs|-UFD}}",
        'UDSRMIN': " = {{Infobox Parti politique français/couleurs|-UDSR}}",
        'UNR': " = {{Infobox Parti politique français/couleurs|-UNR}}",
        'CRR': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'DIVGAUL': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'MRP': " = {{Infobox Parti politique français/couleurs|-MRP}}",
        'MRPVREP': " = {{Infobox Parti politique français/couleurs|-MRP}}",
        'CNI': " = {{Infobox Parti politique français/couleurs|-CNIP}}",
        'MOD': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'EXD': " = {{Infobox Parti politique français/couleurs|-EXD}}",
        'POUJ': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'DIV': " = {{Infobox Parti politique français/couleurs|-DIV}}",
        'PSU': " = {{Infobox Parti politique français/couleurs|-PSU}}",
        'EXG': " = {{Infobox Parti politique français/couleurs|-EXG}}",
        'UNR-UDT': " = {{Infobox Parti politique français/couleurs|-UNR}}",
        'INDVREP': " = {{Infobox Parti politique français/couleurs|-RI}}",
        'FGDS': " = {{Infobox Parti politique français/couleurs|-FGDS}}",
        'RADDROIT': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'UDR': " = {{Infobox Parti politique français/couleurs|-UDR}}",
        'RALLIE': " = {{Infobox Parti politique français/couleurs|-CDP}}",
        'CDP': " = {{Infobox Parti politique français/couleurs|-CDP}}",
        'ALLREP': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'RIUDR': " = {{Infobox Parti politique français/couleurs|-UDR}}",
        'TD': " = {{Infobox Parti politique français/couleurs|-DIV}}",
        'MDR': " = {{Infobox Parti politique français/couleurs|-DIV}}",
        'REG': " = {{Infobox Parti politique français/couleurs|-REG}}",
        'DIVMAJ': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'DVD': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'LO': " = {{Infobox Parti politique français/couleurs|-LO}}",
        'LCR': " = {{Infobox Parti politique français/couleurs|-LCR}}",
        'OCR': " = {{Infobox Parti politique français/couleurs|-COM}}",
        'SOC': " = {{Infobox Parti politique français/couleurs|-PS}}",
        'MRG': " = {{Infobox Parti politique français/couleurs|-PRG}}",
        'DVG': " = {{Infobox Parti politique français/couleurs|-DVG}}",
        'REFRAD': " = {{Infobox Parti politique français/couleurs|-DVG}}",
        'DIVREF': " = {{Infobox Parti politique français/couleurs|-DIV}}",
        'UDRURP': " = {{Infobox Parti politique français/couleurs|-UDR}}",
        'RIURP': " = {{Infobox Parti politique français/couleurs|-RI}}",
        'CDURP': " = {{Infobox Parti politique français/couleurs|-CD}}",
        'CDPURP': " = {{Infobox Parti politique français/couleurs|-CD}}",
        'DIVURP': " = {{Infobox Parti politique français/couleurs|-DVD}}",
        'FRONT': " = {{Infobox Parti politique français/couleurs|-EXG}}",
        'PSMRG': " = {{Infobox Parti politique français/couleurs|-PS}}",
        'ECO': " = {{Infobox Parti politique français/couleurs|-ECO}}",
        'GAULOPP': " = {{Infobox Parti politique français/couleurs|-DIV}}",
        'UDF': " = {{Infobox Parti politique français/couleurs|-UDF}}",
        'RPR': " = {{Infobox Parti politique français/couleurs|-RPR}}",
        'FRN': " = {{Infobox Parti politique français/couleurs|-FN}}",
        'UDF-RPR': " = {{Infobox Parti politique français/couleurs|-UDF}}",
        'CENTDEM': " = {{Infobox Parti politique français/couleurs|-CD}}",
        'OCI': " = {{Infobox Parti politique français/couleurs|-COM}}",
        'RI': " = {{Infobox Parti politique français/couleurs|-RI}}"
    }
    print("| hex", order_number, switcher.get(argument, " =  error"), sep = '')

def couleur_hex_post(col_name, order_number, dictionary):
    if col_name[:5] == 'MODEM':
        print(print_hex(" = {{Infobox Parti politique français/couleurs|-MODEM}}", order_number))
    elif col_name[:5] == 'NouvC':
        print(print_hex(" = {{Infobox Parti politique français/couleurs|-NC}}", order_number))
    elif col_name[:4] == 'PSLE':
        print(print_hex(" = {{Infobox Parti politique français/couleurs|-LC}}", order_number))
    else:
        switch_hex_recent(col_name, dictionary, order_number)

def print_hex(argument, order_number):
    return "| hex" + str(order_number) + argument

def switch_hex_recent(argument, dictionary, order_number):
    switcher = {
        'FDG': print_hex(" = {{Infobox Parti politique français/couleurs|-FG}}", order_number),
        'UMP': print_hex(" = {{Infobox Parti politique français/couleurs|-UMP}}", order_number),
        'UDR': print_hex(" = {{Infobox Parti politique français/couleurs|-UDR}}", order_number),
        'SOC': print_hex(" = {{Infobox Parti politique français/couleurs|-SOC}}", order_number),
        'PRG': print_hex(" = {{Infobox Parti politique français/couleurs|-PRG}}", order_number),
        'RDG': print_hex(" = {{Infobox Parti politique français/couleurs|-PRG}}", order_number),
        'RPR': print_hex(" = {{Infobox Parti politique français/couleurs|-RPR}}", order_number),
        'UDF': print_hex(" = {{Infobox Parti politique français/couleurs|-UDF}}", order_number),
        'GEC': print_hex(" = {{Infobox Parti politique français/couleurs|-GE}}", order_number),
        'SDC': print_hex(" = {{Infobox Parti politique français/couleurs|-PS}}", order_number),
        'VEC': print_hex(" = {{Infobox Parti politique français/couleurs|-Verts}}", order_number),
        'FRN': print_hex(" = {{Infobox Parti politique français/couleurs|-FN}}", order_number),
        'MAJ': print_hex(" = {{Infobox Parti politique français/couleurs|-DIV}}", order_number),
        'ECI': print_hex(" = {{Infobox Parti politique français/couleurs|-DIV}}", order_number),
        'PRV': print_hex(" = {{Infobox Parti politique français/couleurs|-PR}}", order_number),
        'REG': print_hex(" = {{Infobox Parti politique français/couleurs|-REG}}", order_number),
        'EXO': print_hex(" = {{Infobox Parti politique français/couleurs|-EXD}}", order_number),
        'EXG': switch_extremegauche_hex(dictionary[argument], order_number),
        'DVD': switch_diversdroite_hex(dictionary[argument], order_number),
        'DVG': switch_diversgauche_hex(dictionary[argument], order_number),
        'DIV': switch_divers_hex(dictionary[argument], order_number),
        'EXD': switch_extremedroite_hex(dictionary[argument], order_number),
        'ECO': switch_ecologiste_hex(dictionary[argument], order_number),
        'COM': print_hex(" = {{Infobox Parti politique français/couleurs|-COM}}", order_number)
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument[:3], lambda: "error")
    # Execute the function
    print(func)

def switch_extremegauche_hex(argument, order_number):
    switcher = {
        'Lutte Ouvriere': " = {{Infobox Parti politique français/couleurs|-LO}}",
        'Lutte Ouvrière': " = {{Infobox Parti politique français/couleurs|-LO}}",
        'Mouvement Pour Un Parti Des Travailleurs (Mppt)': " = {{Infobox Parti politique français/couleurs|-MPPT}}",
        'Ligue Communiste Revolutionnaire': " = {{Infobox Parti politique français/couleurs|-LCR}}",
        'Nouveau Parti Anticapitaliste': " = {{Infobox Parti politique français/couleurs|-NPA}}",
        'Parti Des Travailleurs': " = {{Infobox Parti politique français/couleurs|-PT}}",
        'Parti Ouvrier Indépendant': " = {{Infobox Parti politique français/couleurs|-POI}}"
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-EXG}}"), order_number)

def switch_diversdroite_hex(argument, order_number):
    switcher = {
        'Mouvement Pour La France': " = {{Infobox Parti politique français/couleurs|-MPF}}",
        'Centre National Des Independants Et Paysans': " = {{Infobox Parti politique français/couleurs|-CNIP}}",
        'Centre National Des Independants': " = {{Infobox Parti politique français/couleurs|-CNIP}}",
        'Debout La Republique': " = {{Infobox Parti politique français/couleurs|-DLF}}",
        'Centre National Des Independants Et Paysans (Cnip)': " = {{Infobox Parti politique français/couleurs|-CNIP}}",
        'Debout La République': " = {{Infobox Parti politique français/couleurs|-DLF}}",
        'Parti Chrétien-Démocrate': " = {{Infobox Parti politique français/couleurs|-PCD}}",
        'Union Républicaine Populaire': " = {{Infobox Parti politique français/couleurs|-UPR}}",
        'Rassemblement Pour La France': " = {{Infobox Parti politique français/couleurs|-RPF}}",
        'Union Des Démocrates Pour La République': " = {{Infobox Parti politique français/couleurs|-UDR}}",
        'Rassemblement Pour La Republique': " = {{Infobox Parti politique français/couleurs|-RPR}}"
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-DVD}}"), order_number)

def switch_diversgauche_hex(argument, order_number):
    switcher = {
        'Socialiste Dissidente': " = {{Infobox Parti politique français/couleurs|-PS}}",
        'empty': " = {{Infobox Parti politique français/couleurs|-DVG}}",
        'Mouvement Des Citoyens': " = {{Infobox Parti politique français/couleurs|-MDC}}",
        'Energie Radicale': " = {{Infobox Parti politique français/couleurs|-PRG}}",
        'Mouvement Républicain Et Citoyen': " = {{Infobox Parti politique français/couleurs|-MRC}}",
        'Parti Socialiste': " = {{Infobox Parti politique français/couleurs|-PS}}",
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-DVG}}"), order_number)

def switch_divers_hex(argument, order_number):
    switcher = {
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = {{Infobox Parti politique français/couleurs|-ECO}}",
        'Chasse Peche Nature Et Traditions': " = {{Infobox Parti politique français/couleurs|-CPNT}}",
        'Chasse Peche Nature Traditions': " = {{Infobox Parti politique français/couleurs|-CPNT}}",
        'Parti Occitan': " = {{Infobox Parti politique français/couleurs|-REG}}",
        "Parti Pirate": " = {{Infobox Parti politique français/couleurs|-violet}}",
        'Sans Etiquette': " = {{Infobox Parti politique français/couleurs|-SE}}",
        'Sans Étiquette': " = {{Infobox Parti politique français/couleurs|-SE}}",
        'Regionalistes': " = {{Infobox Parti politique français/couleurs|-REG}}",
        "Reseau Nouvelle Donne": " = {{Infobox Parti politique français/couleurs|-fuchsia}}",
        "Union Democratique Bretonne": " = {{Infobox Parti politique français/couleurs|-UDB}}",
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-DIV}}"), order_number)

def switch_extremedroite_hex(argument, order_number):
    switcher = {
        'Mouvement National Republicain': " = {{Infobox Parti politique français/couleurs|-MNR}}",
        "Mnr - Contre L'Immigration-Islamisation, L'Insecurite": " = {{Infobox Parti politique français/couleurs|-MNR}}",
        "Mnr - Contre L'Immigration-Islamisation": " = {{Infobox Parti politique français/couleurs|-MNR}}",
        'Mouvement National Republicain': " = {{Infobox Parti politique français/couleurs|-MNR}}",
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-EXD}}"), order_number)

def switch_ecologiste_hex(argument, order_number):
    switcher = {
        'Generation Ecologie': " = {{Infobox Parti politique français/couleurs|-GE}}",
        'Les Verts': " = {{Infobox Parti politique français/couleurs|-Verts}}",
        'Europe-Ecologie-Les Verts': " = {{Infobox Parti politique français/couleurs|-EELV}}",
        'Alliance Ecologiste Indépendante': " = {{Infobox Parti politique français/couleurs|-AEI}}",
        'Mouvement Ecologiste Independant': " = {{Infobox Parti politique français/couleurs|-MEI}}",
        'Mouvement Écologiste Indépendant': " = {{Infobox Parti politique français/couleurs|-MEI}}"
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-ECO}}"), order_number)

def partie_name(argument, order_number):
    switcher = {
        'COM': " = [[Parti communiste français|PCF]]",
        'COM2': " = [[Apparentement|app.]] [[Parti communiste français|PCF]]",
        'UFD': " = [[Union des forces démocratiques (France)|UFD]]",
        'SFIO': " = [[Section française de l'Internationale ouvrière|SFIO]]",
        'RADSOC': " = [[Parti radical (France)|RADSOC]]",
        'RADICAUX GAUCHE': " = [[Parti radical (France)|RADSOC]]",
        'RADCENT': " = Radicaux centristes",
        'RADUFD': " = Radicaux de l'[[Union des forces démocratiques (France)|UFD]]",
        'UDSRMIN': " = [[Union démocratique et socialiste de la Résistance|UDSR]]",
        'UNR': " = [[Union pour la nouvelle République|UNR]]",
        'CRR': " = [[Centre républicain|CR]]",
        'DIVGAUL': " = Divers gaullistes",
        'MRP': " = [[Mouvement républicain populaire|MRP]]",
        'MRPVREP': " = [[Mouvement républicain populaire|MRP]]",
        'CNI': " = [[Centre national des indépendants et paysans|CNIP]]",
        'MOD': " = [[Républicains modérés|Modérés]]",
        'EXD': " = [[Extrême droite en France|EXD]]",
        'POUJ': " = [[Poujadisme|Poujadistes]]",
        'DIV': " = Divers",
        'PSU': " = [[Parti socialiste unifié (France)|PSU]]",
        'EXG': " = [[Extrême gauche en France|EXG]]",
        'UNR-UDT': " = [[Union pour la nouvelle République|UNR-UDT]]",
        'INDVREP': " = [[Fédération nationale des républicains indépendants|RI]]",
        'FGDS': " = [[Fédération de la gauche démocrate et socialiste|FGDS]]",
        'RADDROIT': " = Radicaux de droite",
        'UDR': " = [[Union des démocrates pour la République|UDR]]",
        'RALLIE': " = [[Centre démocratie et progrès|CDP]]",
        'CDP': " = [[Centre démocratie et progrès|CDP]]",
        'ALLREP': " = [[Alliance républicaine pour les libertés et le progrès|AR]]",
        'RIUDR': " = [[Fédération nationale des républicains indépendants|RI]]-[[Union des démocrates pour la République|UDR]]",
        'TD': " = Technique et démocratie",
        'MDR': " = [[Mouvement des réformateurs|MR]]",
        'REG': " = [[Régionalisme (politique)|REG]]",
        'DIVMAJ': " = [[Divers droite|DVD]]",
        'DVD': " = [[Divers droite|DVD]]",
        'LO': " = [[Lutte ouvrière|LO]]",
        'LCR': " = [[Ligue communiste révolutionnaire|LCR]]",
        'OCR': " = [[Organisation communiste révolutionnaire|OCR]]",
        'SOC': " = [[Parti socialiste (France)|PS]]",
        'MRG': " = [[Parti radical de gauche|MRG]]",
        'DVG': " = [[Divers gauche|DVG]]",
        'REFRAD': " = Radicaux réformateurs",
        'DIVREF': " = Divers réformateurs",
        'UDRURP': " = [[Union des démocrates pour la République|UDR]]-[[Union des républicains de progrès|URP]]",
        'RIURP': " = [[Fédération nationale des républicains indépendants|RI]]-[[Union des républicains de progrès|URP]]",
        'CDURP': " = [[Centre démocrate (France)|CD]]-[[Union des républicains de progrès|URP]]",
        'CDPURP': " = [[Centre démocrate (France)|CD]]-[[Union des républicains de progrès|URP]]",
        'DIVURP': " = Divers [[Union des républicains de progrès|URP]]",
        'FRONT': " = Front Autogestionnaire",
        'PSMRG': " = [[Parti socialiste (France)|PS]]-[[Parti radical de gauche|PRG]]",
        'ECO': " = [[Écologie politique|ECO]]",
        'GAULOPP': " = Gaullistes d'opposition",
        'UDF': " = [[Union pour la démocratie française|UDF]]",
        'RPR': " = [[Rassemblement pour la République|RPR]]",
        'FRN': " = [[Rassemblement national|FN]]",
        'UDF-RPR': " = [[Union pour la démocratie française|UDF]]-[[Rassemblement pour la République|RPR]]",
        'CENTDEM': " = [[Centre démocrate (France)|CD]]",
        'OCI': " = [[Organisation communiste révolutionnaire|OCI]]",
        'RI': " = [[Fédération nationale des républicains indépendants|RI]]"
    }
    print(print_partie(switcher.get(argument, " =  error"), order_number))

def partie_name_post(col_name, order_number, dictionary):
    if col_name[:5] == 'MODEM':
        print(print_partie(" = [[Mouvement démocrate (France)|MODEM]]", order_number))
    elif col_name[:5] == 'NouvC':
        print(print_partie(" = [[Les Centristes|LC]]", order_number))
    elif col_name[:4] == 'PSLE':
        print(print_partie(" = [[Les Centristes|PSLE]]", order_number))
    else:
        switch_partie_recent(col_name, dictionary, order_number)

def print_partie(argument, order_number):
    return "| parti" + str(order_number) + argument

def switch_partie_recent(argument, dictionary, order_number):
    switcher = {
        'ECI': print_partie(" = {{abréviation|DIV|Divers}}", order_number),
        'PRV': print_partie(" = [[Parti radical (France)|PRV]]", order_number),
        'MAJ': print_partie(" = Majorité Présidentielle", order_number),
        'FRN': print_partie(" = [[Rassemblement national|FN]]", order_number),
        'VEC': print_partie(" = [[Les Verts (France)|LV]]", order_number),
        'GEC': print_partie(" = [[Génération écologie|GE]]", order_number),
        'UDF': print_partie(" = [[Union pour la démocratie française|UDF]]", order_number),
        'RPR': print_partie(" = [[Rassemblement pour la République|RPR]]", order_number),
        'PRG': print_partie(" = [[Parti radical de gauche|PRG]]", order_number),
        'RDG': print_partie(" = [[Parti radical de gauche|PRG]]", order_number),
        'SOC': print_partie(" = [[Parti socialiste (France)|PS]]", order_number),
        'SCO': print_partie(" = [[Parti socialiste (France)|PS]]", order_number),
        'SDC': print_partie(" = [[Parti socialiste (France)|PS]]", order_number),
        'UMP': print_partie(" = [[Union pour un mouvement populaire|UMP]]", order_number),
        'UDR': print_partie(" = [[Union des démocrates pour la République|UDR]]", order_number),
        'FDG': print_partie(" = [[Front de gauche (France)|FDG]]", order_number),
        'EXO': switch_exocode(dictionary[argument], order_number),
        'REG': switch_regionalisme(dictionary[argument], order_number),
        'EXG': switch_extremegauche(dictionary[argument], order_number),
        'DVD': switch_diversdroite(dictionary[argument], order_number),
        'DVG': switch_diversgauche(dictionary[argument], order_number),
        'DIV': switch_divers(dictionary[argument], order_number),
        'EXD': switch_extremedroite(dictionary[argument], order_number),
        'ECO': switch_ecologiste(dictionary[argument], order_number),
        'COM': switch_communiste(dictionary[argument], order_number)
    }
    print(switcher.get(argument[:3], lambda: "error"))

def switch_exocode(argument, order_number):
    switcher = {
        'empty': " = Error",
        'Parti ouvrier européen': " = [[Parti ouvrier européen|POE]]"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_regionalisme(argument, order_number):
    switcher = {
        'empty': " = [[Régionalisme (politique)|REG]]",
        'Unitat Catalana': " = [[Unitat Catalana|UC]]",
        'Abertzaleen Batasuna':  " = [[Abertzaleen Batasuna|AB]]",
        'Union Du Peuple Alsacien':  " = [[Union du peuple alsacien|UPA]]",
        'Abertzale Nationaliste Basque':  " = [[Abertzaleen Batasuna|AB]]",
        'Abertzale Nationaliste Basque':  " = [[Abertzaleen Batasuna|AB]]",
        "Alsace D'Abord, Pour L'Europe Des Regions":  " = [[Alsace d'abord|AA]]",
        "Alsace D'Abord":  " = [[Alsace d'abord|AA]]",
        'Erc (Esquarra Republicana Catalana)':  " = [[Gauche républicaine de Catalogne|GRC]]",
        "Ea Cusko Alkartasuna": " = {{abréviation|ECA|Ea Cusko Alkartasuna}}",
        "La Radio Des Alsaciens 107 4 Mhz": " = {{abréviation|RA107.4|La radio des alsaciens 107.4 Mhz}}",
        "Radio Alsaciens 107 4 Mhz": " = {{abréviation|RA107.4|La radio des alsaciens 107.4 Mhz}}",
        "Entente Des Ecologistes, Les Verts": " = {{abréviation|EE|Entente des écologistes}}-[[Les Verts (France)|LV]]"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_extremegauche(argument, order_number):
    switcher = {
        'empty': " = [[Extrême gauche en France|EXG]]",
        'Divers': " = [[Extrême gauche en France|EXG]]",
        'Lutte Ouvrière': " = [[Lutte ouvrière|LO]]",
        'Lutte Ouvriere': " = [[Lutte ouvrière|LO]]",
        'Parti Humaniste': " = [[Parti humaniste (France)|PH]]",
        'Candidate Du Parti Humaniste': " = [[Parti humaniste (France)|PH]]",
        'Alternative Democratie Socialisme': " = [[Convention pour une alternative progressiste|ADS]]",
        'Candidat De Lutte Ouvriere': " = [[Lutte ouvrière|LO]]",
        'Ligue Communiste Revolutionnaire': " = [[Ligue communiste révolutionnaire|LCR]]",
        'Ligue Communiste Revolutionnaire (Dissident)': " = {{abréviation|diss|dissident}} [[Ligue communiste révolutionnaire|LCR]]",
        'Nouveau Parti Anticapitaliste': " = [[Nouveau Parti anticapitaliste|NPA]]",
        'Alternatifs (Solidarite, Ecologie, Gauche Alternative)': " = [[Les Alternatifs]]",
        'Gauche Alternative Et Ecologiste': " = [[Les Alternatifs]]",
        'Les Alternatifs': " = [[Les Alternatifs]]",
        'Extreme Gauche': " = [[Extrême gauche en France|EXG]]",
        'Extrême gauche': " = [[Extrême gauche en France|EXG]]",
        'Parti Pour La Décroissance': " = [[Parti pour la décroissance|PPLD]]",
        'Parti Des Travailleurs': " = [[Parti des travailleurs (France)|PT]]",
        'Parti Des Travailâ­Leurs': " = [[Parti des travailleurs (France)|PT]]",
        'Mouvement De La Gauche Progressiste': " = [[Mouvement de la gauche progressiste|MGP]]",
        'Gauche Alternative 2007': " = [[Gauche alternative 2007|GP2007]]",
        'A Gauche Autrement, Sega (Solidarite, Ecologie, Gauche Alternative)': " = {{abréviation|GA|A gauche autrement}}-[[Gauche alternative 2007|GP2007]]",
        'Alternative Rouge Et Verte': " = [[Alternative rouge et verte|ARV]]",
        'Ligue Trotskiste': " = [[Ligue trotskiste de France|LT]]",
        'Mouvement Pour Un Parti Des Travailleurs (Mppt)': " = [[Mouvement pour un parti des travailleurs|MPPT]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Solidarite, Ecologie, Gauche Alternative (Sega)': " = [[Gauche alternative 2007|SEGA]]",
        'Solidarite Ecologie Gauche Alternative (Sega)': " = [[Gauche alternative 2007|SEGA]]",
        'Solidarite, Ecologie Gauche Alternative': " = [[Gauche alternative 2007|SEGA]]",
        'Solidarite Ecologie Gauche Alternative': " = [[Gauche alternative 2007|SEGA]]",
        'Solidarite Ecologie, Gauche Alternative': " = [[Gauche alternative 2007|SEGA]]",
        "Mouvement Ecologiste De L'Anjou, Solidarite, Ecologie Gauche Alternative (Sega)": " = {{abréviation|MEA|Mouvement Ecologiste de l'Anjou}}-[[Gauche alternative 2007|SEGA]]",
        'Candidat D Initiative Pour Une Nouvelle Politique A Gauche': " = {{abréviation|CINPG|Candidat d'initiative pour une nouvelle politique à gauche}}",
        'Voix Des Travailleurs': " = [[Voix des travailleurs|VdT]]",
        'Les Alternatifs-Ecologie-Autogestion': " = [[Les Alternatifs]]-Ecologie-Autogestion",
        "Gauche Alternative 2012": " = {{abréviation|GA2012|Gauche Alternative 2012}}",
        "A Gauche Autrement": " = {{abréviation|GA|A Gauche Autrement}}",
        "Gauche Revolutionnaire": " = {{abréviation|GR|Gauche Révolutionnaire}}",
        "Parti Des Chomeurs Et Des Mecontents": " = {{abréviation|CM|Parti des chômeurs et des mécontents}}",
        "Opposition Ouvriere": " = {{abréviation|OO|Opposition Ouvrière}}",
        "Ligue Socialiste Des Travailleurs": " = {{abréviation|LST|Ligue Socialiste des Travailleurs}}",
        "Ecologie Pacifisme Objection De Croissance": " = {{abréviation|EPOC|Écologie pacifisme objection de croissance}}",
        "Changer A Gauche": " = {{abréviation|CG|Changer à gauche}}",
        "Comite Pour La Defense Du Regime Local": " = {{abréviation|CDRL|Comite pour la défense du régime local}}",
        "Candidatures Unitaires Antiliberales 79": " = {{abréviation|UA79|Unitaires Antiliberales 79}}",
        "Tous Ensemble A Gauche": " = {{abréviation|TEG|Tous ensemble à gauche}}",
        "Collectif Antiliberal Du Pays De Lorient": " = {{abréviation|CG|Collectif antilibéral du pays de Lorient}}",
        "100% A Gauche - Lcr": " = {{abréviation|100%|100% à gauche}}-[[Ligue communiste révolutionnaire|LCR]]",
        "L.C.R. 100% A Gauche": " = {{abréviation|100%|100% à gauche}}-[[Ligue communiste révolutionnaire|LCR]]",
        "Union Pour L'Ecologie Et La Democratie": " = {{abréviation|UED|Union pour l'écologie et la démocratie}}",
        "Autogestion Soutenu Par Les Verts": " = {{abréviation|ALV|Autogestion soutenu par Les Verts}}",
        "Anjou Ecologie Autogestion": " = {{abréviation|AEA|Anjou Ecologie Autogestion}}",
        "A Gauche Toute Collectif Pour Une Gauc": " = {{abréviation|GCG|A Gauche toute Collectif pour une Gauche}}",
        "Pole Rennaissance Communiste En France": " = [[Pôle de renaissance communiste en France|PRCF]]",
        'Union Pour La Gauche Renovee': " = {{abréviation|UGR|Union pour la gauche rénovée}}",
        'Initiative Pour Une Nouvelle Politique Gauche': " = {{abréviation|INPG|Initiative pour une nouvelle politique gauche}}",
        'Candidat D Initiative Pour Une Nouvelle Politique De Gauche': " = {{abréviation|INPG|Initiative pour une nouvelle politique gauche}}",
        'Tous Ensemble A Gauche': " = {{abréviation|TEG|Tous ensemble à gauche}}",
        "Parti Ouvrier Indépendant": " = [[Parti ouvrier indépendant|POI]]",
        'A Gauche Vraiment': " = {{abréviation|GV|A gauche vraiment}}",
        'Gauche 92 Cap': " = {{abréviation|G92C|Gauche 92 Cap}}",
        'Gauche 92': " = {{abréviation|G92|Gauche 92}}",
        'Gauche 92 Les Alternatifs': " = [[Les Alternatifs]]",
        'Parti De Gauche Dissident': " = {{abréviation|diss.|dissident}} [[Parti de gauche (France)|PG]]",
        'Gauche Citoyenne Et Ecologiste': " = {{abréviation|GCE|Gauche Citoyenne et Ecologiste}}",
        'Mouvement A Gauche Vraiment': " = {{abréviation|GV|A gauche vraiment}}",
        'Gauche Unitaire Et Antiliberale': " = {{abréviation|GUA|Gauche Unitaire et Antilibérale}}",
        'Gauche Alternative': " = {{abréviation|GA|Gauche Alternative}}",
        'Yvelines Décroissance': " = {{abréviation|YD|Yvelines Décroissance}}",
        'Parti Des Evidences Concretes': " = {{abréviation|PEC|Parti des Évidences Concrètes}}",
        'Pour Une Nouvelle Politique A Gauche': " = {{abréviation|NPG|Pour une nouvelle politique à gauche}}",
        'Pour L Initiative Pour Une Nouvelle Politique A Gauche': " = {{abréviation|NPG|Pour l'initiative pour une nouvelle politique à gauche}}",
        'Rassemblement Utile A Tous': " = {{abréviation|RUT|Rassemblement utile à tous}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_diversdroite(argument, order_number):
    switcher = {
        'empty': " = [[Divers droite|DVD]]",
        'Union Pour Un Mouvement Populaire': " = [[Union pour un mouvement populaire|UMP]]",
        'Union Pour La Majorite Presidentielle': " = [[Union pour un mouvement populaire|UMP]]",
        'Parti Republicain': " = [[Parti républicain (France)|PR]]",
        'Mouvement Pour La France': " = [[Mouvement pour la France|MPF]]",
        'Debout La République': " = [[Debout la France|DLR]]",
        'Royaliste': " = [[Royalisme|Royaliste]]",
        'Debout La Republique': " = [[Debout la France|DLR]]",
        'Royaliste D Action Francaise': " = [[Action française|AF]]",
        'Moselle Debout Rpr-Udf-Cnip': " = {{abréviation|MD|Moselle Debout}}-[[Centre national des indépendants et paysans|CNIP]]-[[Union pour la démocratie française|UDF]]-[[Rassemblement pour la République|RPR]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Sans Étiquette (Soutien Ump Et Prv)': " = [[Sans étiquette|SE]] ([[Union pour un mouvement populaire|UMP]]-[[Parti républicain (France)|PR]])",
        'Membre Du Centre National Des Independants': " = [[Centre national des indépendants et paysans|CNI]]",
        'Centre National Des Independants Et Paysans': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Centre National Des Independants Et Paysans (Cni)': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Centre National Des Independants Et Paysans (Cnip)': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Cnip': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Centre National Des Independants': " = [[Centre national des indépendants et paysans|CNI]]",
        'Droite De Conviction Pour La Defense Des Valeurs': " = {{abréviation|DCDV|Droite de conviction pour la défense des valeurs}}",
        'Droite De Conviction Pour La Defense Des Valeurs Presente Par Le Centre National Des Independants Et Paysans Cni': " = {{abréviation|DCDV|Droite de conviction pour la défense des valeurs}}-[[Centre national des indépendants et paysans|CNI]]",
        'Droite De Conviction Pour La Defense Des Valeurs Presente Par Le Centre National Des Independants Et Paysans (Cni) Et La Democratie Chretienne Francaise (Dcf)': " = {{abréviation|DCDV|Droite de conviction pour la défense des valeurs}}-[[Centre national des indépendants et paysans|CNI]]-{{abréviation|DCF|Démocratie Chrétienne Française}}",
        'Parti Chrétien-Démocrate': " = [[VIA, la voie du peuple|PCD]]",
        'Union Républicaine Populaire': " = [[Union populaire républicaine (2007)|UPR]]",
        'Divers Droite': " = [[Divers droite|DVD]]",
        'Lyon Divers Droite (Soutien Pcd Et Mpf)': " = [[Divers droite|DVD]]",
        'Lyon Divers Droite': " = [[Divers droite|DVD]]",
        'La Droite Independante (Mpf)': " = [[La droite indépendante|LDI]]",
        'Rassemblement Pour La France': " = [[Rassemblement pour la France|RPF]]",
        'Mouvement Des Reformateur': " = [[Mouvement des réformateurs|MR]]",
        'Union Des Démocrates Pour La République': " = [[Union des démocrates pour la République|UDR]]",
        'Mouvement De M. Jeannou Lacaze Candidat Union Des Democrates': " = [[Union des démocrates pour la République|UDR]]",
        'Rassemblement Pour La Republique': " = [[Rassemblement pour la République|RPR]]",
        "Union De L'Opposition Udf-Rpr": " = [[Union pour la démocratie française|UDF]]-[[Rassemblement pour la République|RPR]]",
        'Renouveau Du Mantois, Centre National Des Independants Et Paysans': " = {{abréviation|RM|Renouveau du Mantois}} [[Centre national des indépendants et paysans|CNIP]]",
        "Udf Dissident": " = {{abréviation|diss.|dissident}} [[Union pour la démocratie française|UDF]]",
        "Union Pour Un Mouvement Populaire (Dissident)": " = {{abréviation|diss.|dissident}} [[Union pour un mouvement populaire|UMP]]",
        'Majorite Presidentielle - Rpr': " = [[Rassemblement pour la République|RPR]]",
        'Rpr Dissident': " = {{abréviation|diss.|dissident}} [[Rassemblement pour la République|RPR]]",
        'Rassemblement Pour La Republique Dissident': " = {{abréviation|diss.|dissident}} [[Rassemblement pour la République|RPR]]",
        'Droite Liberale Chretienne': " = [[Droite libérale-chrétienne|DLC]]",
        'Alternative Liberale': " = [[Alternative libérale|AL]]",
        'Alliance Royale': " = [[Alliance royale|AR]]",
        'Parti De La Loi Naturelle': " = [[Parti de la loi naturelle|PLN]]",
        'Candidat Du Parti Democrate Francais': " = [[Parti démocrate français|PDF]]",
        'Le Trefle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Union De La Droite Republicaine': " = Union de la droite republicaine",
        'Mouvement Des Reformateurs': " = [[Mouvement des réformateurs|MDR]]",
        'Renouveau Centriste': " = {{abréviation|RC|Renouveau Centriste}}",
        'Mouvement Social Democrate': " = {{abréviation|MSD|Mouvement Social Démocrate}}",
        'Centre Chretien Populaire': " = {{abréviation|CCP|Centre Chretien Populaire}}",
        "Candidat Independant D'Opposition": " = {{abréviation|CIO|Candidat Indépendant d'Opposition}}",
        "Candidature Liberale": " = {{abréviation|CL|Candidature Libérale}}",
        "Alternative Region Mantaise": " = {{abréviation|ARM|Alternative Région Mantaise}}",
        "Association Des Usagers De L'Administration": " = {{abréviation|AUA|Association des usagers de l'administration}}",
        "Candidate Presentee Par L'Union Des Independants": " = {{abréviation|UI|Union des Indépendants}}",
        'Entente Souverainiste': " = {{abréviation|ES|Entente Souverainiste}}",
        "Appel Du 7 Mai Pour L'Union De La Majorite Presidentielle": " = {{abréviation|MP|Appel du 7 Mai pour l'union de la Majorité Présidentielle}}",
        'Union De La Droite En Mouvement': " = {{abréviation|UDM|Union de la Droite en Mouvement}}",
        'Candidat Pour La Defense Du 14 Eme': " = {{abréviation|D14|Candidat pour la défense du 14éme}}",
        'Union De La Jeunesse Et Des Createurs': " = {{abréviation|UJC|Union de la Jeunesse et des Créateurs}}",
        'Candidat Republicain Du Beaujolais': " = {{abréviation|CRB|Candidat républicain du Beaujolais}}",
        'Alliance Radicale Et Centriste': " = {{abréviation|ARC|Alliance radicale et centriste}}",
        'Union Centriste Liberale Et Republicaine': " = {{abréviation|UCLR|Union Centriste Libérale et Républicaine}}",
        'Objectif Decroissance': " = {{abréviation|OD|Objectif Décroissance}}",
        'Parti Picard Democrate': " = {{abréviation|PPD|Parti Picard Démocrate}}",
        'Union France Democratie': " = {{abréviation|UFD|Union France Démocratie}}",
        'Parti Des Francophones': " = {{abréviation|PF|Parti des Francophones}}",
        'Democrate Du Centre Libre': " = {{abréviation|DCL|Démocrate du centre libre}}",
        'Rassemblement Democrate Et Liberal': " = {{abréviation|RDL|Rassemblement Démocrate et Libéral}}",
        'Pour Un Vrai Changement Liberal': " = {{abréviation|VCL|Pour un vrai changement libéral}}",
        "Aujourd'Hui, Autrement": " = {{abréviation|AA|Aujourd'Hui, Autrement}}",
        'Rassemblement Social Et Liberal': " = {{abréviation|RSL|Rassemblement Social et Libéral}}",
        'Comite L Alsace Merite Mieux': " = {{abréviation|CAMM|Comite l'Alsace mérite mieux}}",
        'Rassemblement Des Democrates Et Des Republicains De Progres': " = {{abréviation|RDRP|Rassemblement des démocrates et des républicains de progrès}}",
        'Union Pour La Democratie Francaise Dissident': " = {{abréviation|UDFD|Union pour la démocratie française dissident}}",
        'Pour L Union Des Partis Politiques Francais': " = {{abréviation|UPPF|Pour l'union des partis politiques francais}}",
        'Federation Des Independants Du Bas Rhin Cin': " = {{abréviation|FIBR|Fédération des indépendants du Bas-Rhin}}",
        'Cand. Indept  Defense Du Monde Rural': " = {{abréviation|CIDMR|Candidat Indépendent défense du monde rural}}",
        'Union Centriste Republicaine': " = {{abréviation|UCR|Union Centriste Républicaine}}",
        "Ensemble, L'An 2000": " = {{abréviation|EA2000|Ensemble, l'an 2000}}",
        "Independant De L'Opposition": " = {{abréviation|IO|Indépendant de l'opposition}}",
        "Rassemblement Pour L'Independance De L'Europe": " = {{abréviation|RIE|Rassemblement pour l'indépendance de l'Europe}}",
        'Dvd Union De La Droite - Mp': " = {{abréviation|UD-MP|Union de la droite - MP}}",
        'Union Centriste': " = {{abréviation|UC|Union Centriste}}",
        'Rassemblement Des Independants': " = {{abréviation|RI|Rassemblement des indépendants}}",
        'Parti Blanc': " = {{abréviation|PB|Parti Blanc}}",
        'Union Nationale Des Electeurs': " = {{abréviation|UNE|Union Nationale des Electeurs}}",
        "Independant D'Opposition": " = {{abréviation|IO|Indépendant d'opposition}}",
        "Union Royaliste": " = {{abréviation|UR|Union Royaliste}}",
        "Mouvement Servir": " = {{abréviation|MS|Mouvement Servir}}",
        "Mouvement France Regions (Mfr)": " = {{abréviation|MFR|Mouvement France Régions}}",
        'Union De Rassemblement Et Du Centre': " = {{abréviation|URC|Union de Rassemblement et du Centre}}",
        'Moselle Debout, Nouvelle Generation Lorraine': " = {{abréviation|MDNGL|Moselle Debout, Nouvelle Génération Lorraine}}",
        'Gaulliste De Progres Social': " = {{abréviation|GPS|Gaulliste de progrés social}}",
        'Droite Independant': " = {{abréviation|DI|Droite Indépendant}}",
        'Union Des Producteurs De Porc Des Pyrenees Altlantiques': " = {{abréviation|UPPPA|Union des producteurs de porc des Pyrénées-Altlantiques}}",
        'Union Des Producteurs De Porcs Des Pyrenees Atlantiques': " = {{abréviation|UPPPA|Union des producteurs de porc des Pyrénées-Altlantiques}}",
        'Democratie Permanente': " = {{abréviation|DP|Démocratie permanente}}",
        'Union Pour Une Politique Nouvelle': " = {{abréviation|UPN|Union pour une Politique Nouvelle}}",
        'Association De Defense Des Locataires': " = {{abréviation|ADL|Association de Défense des Locataires}}",
        'Parti Pour La Liberte': " = {{abréviation|PL|Parti pour la liberté}}",
        "Valeur D'Inspiration Chrétienne, Sociale, Écologique Et Diversité": " = {{abréviation|VICSED|Valeur d'inspiration chrétienne, sociale, écologique et diversité}}",
        'Centriste De Progres': " = {{abréviation|CP|Centriste de progrès}}",
        'Morale Politique Verite': " = {{abréviation|MPV|Morale Politique Vérité}}",
        'Gaulliste D`Opposition Nationale': " = {{abréviation|GON|Gaulliste d'Opposition Nationale}}",
        'Independant Pour Une Lorraine Forte': " = {{abréviation|ILF|Independant pour une Lorraine forte}}",
        'Independant De Droite': " = {{abréviation|ID|Indépendant de droite}}",
        'Gaulliste Social': " = {{abréviation|GS|Gaulliste Social}}",
        'Droite Unifiee': " = {{abréviation|DU|Droite Unifiée}}",
        'Rhône Divers Droite': " = {{abréviation|RDD|Rhône Divers Droite}}",
        'Divers Droite Liberale Et Sociale': " = {{abréviation|DDLS|Divers droite libérale et sociale}}",
        'Union Nationale Republicaine': " = {{abréviation|UNR|Union Nationale Républicaine}}",
        'Parti Liberal Chretien': " = {{abréviation|PLC|Parti Libéral Chretien}}",
        "Mouvement Democrate Francais": " = {{abréviation|MDF|Mouvement Démocrate Français}}",
        'Mouvement Des Democrates': " = {{abréviation|MD|Mouvement des démocrates}}",
        'Gaulliste Independant': " = {{abréviation|GI|Gaulliste Indépendant}}",
        'Pour La Justice Et La Prosperite De La France': " = {{abréviation|JPF|Pour la justice et la prospérité de la France}}",
        'Union Des Independants': " = {{abréviation|UI|Union des Indépendants}}",
        "Candidat Presente Par L'Union Des Independants Mouvement De M. Jeannou Lacaze": " = {{abréviation|UI|Union des Indépendants}}",
        'Cap Liberte Egalite Fraternite': " = {{abréviation|CLEF|Cap Liberté Egalité Fraternité}}",
        'Union Du Rassemblement Et Du Centre': " = {{abréviation|URC|Union du rassemblement et du centre}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_diversgauche(argument, order_number):
    switcher = {
        'Divers Gauche': " = [[Divers gauche|DVG]]",
        'empty': " = [[Divers gauche|DVG]]",
        'Pole Republicain': " = [[Pôle républicain|PR]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Mouvement Republicain Et Citoyen': " = [[Mouvement républicain et citoyen|MRC]]",
        'Mouvement Republicain Et Citoyen (Soutien Ps)': " = [[Mouvement républicain et citoyen|MRC]]",
        'Socialiste Dissidente': " = [[Dissidence|diss]] [[Parti socialiste (France)|PS]]",
        'Parti Socialiste (Dissident)': " = [[Dissidence|diss]] [[Parti socialiste (France)|PS]]",
        'Pour La Semaine De 4 Jours': " = [[Semaine de quatre jours|Pour la semaine de 4 jours]]",
        'Mouvement Des Citoyens': " = [[Mouvement des citoyens (France)|MDC]]",
        'Mouvement Des Citoyens Soutien Parti Communiste Francais': " = [[Mouvement des citoyens (France)|MDC]]-[[Parti communiste français|PCF]]",
        'Energie Radicale': " = [[Mouvement des citoyens (France)|MDC]]",
        'Mouvement Républicain Et Citoyen': " = [[Mouvement républicain et citoyen|MRC]]",
        'Parti Socialiste': " = [[Parti socialiste (France)|PS]]",
        'Regions Et Peuples Solidaires': " = [[Régions et peuples solidaires|RPS]]",
        'Pole Republicain Et Udf': " = [[Pôle républicain|PR]]-[[Union pour la démocratie française|UDF]]",
        'Divers Gauche Et Centre': " = [[Divers gauche|DVG]]",
        'Dissident Parti Radical De Gauche': " = {{abréviation|diss.|dissident}} [[Parti radical de gauche|PRG]]",
        "Rassemblement Pour Initiative Citoyenne": " = {{abréviation|RIC|Rassemblement pour l'initiative citoyenne}}",
        "Mouvement Republique Et Democratie": " = {{abréviation|MRD|Mouvement république et démocratie}}",
        'Republique Et Democratie': " = {{abréviation|RD|République et démocratie}}",
        'Force Libertes': " = {{abréviation|FL|Force Libertés}}",
        'Mars-Gauche Republicaine': " = {{abréviation|MGR|Mars-Gauche Républicaine}}",
        'Mouvement Democratie Alsacienne': " = {{abréviation|MDA|Mouvement Démocratie Alsacienne}}",
        'Gauche Solidaire': " = {{abréviation|GS|Gauche Solidaire}}",
        'Socialiste Dissident': " = {{abréviation|SD|Socialiste Dissident}}",
        'Citoyennete Pour Tous De Maine-Et-Loire': " = {{abréviation|CML|Citoyennete pour tous de Maine-et-Loire}}",
        'Candidat Des Forces De Gauche, Ecologistes Et Republicains De Progres': " = {{abréviation|CFGERP|Candidat des Forces de Gauche, Ecologistes et Républicains de Progrés}}",
        'Gauche Independante': " = {{abréviation|GI|Gauche indépendante}}",
        'Gaulliste De Gauche': " = {{abréviation|GG|Gaulliste de Gauche}}",
        'Nouvelle Gauche': " = {{abréviation|NG|Nouvelle Gauche}}",
        'Nouvelle Vague - Dvg': " = {{abréviation|NV-DVG|Nouvelle Vague - DVG}}",
        'La Force Salarienne': " = {{abréviation|FS|La Force Salarienne}}",
        'Centre Gauche': " = {{abréviation|CG|Centre Gauche}}",
        'Alternative Unitaire Antiliberale': " = {{abréviation|AUA|Alternative Unitaire Antilibérale}}",
        'Gauche Nouvelle, Audacieuse, Realiste': " = {{abréviation|GNAR|Gauche Nouvelle, Audacieuse, Réaliste}}",
        'Carrefour Des Gauches': " = {{abréviation|CG|Carrefour des gauches}}",
        'Gauche Ouvriere Et Chretienne': " = {{abréviation|GOC|Gauche ouvrière et chrétienne}}",
        'Convention Pour Une Alternative Progressive': " = {{abréviation|CAP|Convention pour une alternative progressive}}",
        'Citoyens En Mouvement': " = {{abréviation|CM|Citoyens en Mouvement}}",
        'Mouvement Democratie Lorraine': " = {{abréviation|MDL|Mouvement Démocratie Lorraine}}",
        'Renouveau A Gauche': " = {{abréviation|RG|Renouveau à Gauche}}",
        'A Gauche Vraiment': " = {{abréviation|GV|A Gauche Vraiment}}",
        'Initiative Republicaine': " = {{abréviation|IR|Initiative républicaine}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_divers(argument, order_number):
    switcher = {
        'empty': " = Divers",
        'Le Trefle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|NE]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecologistes Hommes Nature Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Representante Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecoloâ­Gistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecoâ­Logistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux, Union Nationale Ecologiste': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        "Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux, Presentes Par L'Union Nationale Ecologiste, Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        "Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux Presentes Par L'Union Nationale Ecologiste, Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        "Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux Presente Par L'Union Nationale Ecologiste Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste Union Nationale Ecologiste": " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Parti De La Loi Naturelle': " = [[Parti de la loi naturelle|PLN]]",
        'La Loi Naturelle': " = [[Parti de la loi naturelle|PLN]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Sans Étiquette': " = [[Sans étiquette|SE]]",
        'Euskal Herria Bai': " = [[Euskal Herria Bai|EHBai]]",
        'Esquerra Republicana De Catalunya': " = [[Gauche républicaine de Catalogne|GRC]]",
        'Batasuna': " = [[Batasuna]]",
        "Mouvement Regionaliste Alsace D'Abord": " = [[Alsace d'abord|AA]]",
        'Unitat Catalana': " = [[Unitat Catalana|UC]]",
        'Convergence Democratique De Catalogne': " = [[Convergence démocratique de Catalogne|UDC]]",
        'Parti Nationaliste Basque': " = [[Parti nationaliste basque (France)|PNB]]",
        'Chasse Peche Nature Traditions': " = [[Le Mouvement de la ruralité|CPNT]]",
        'Chasse Peche Nature Et Traditions': " = [[Le Mouvement de la ruralité|CPNT]]",
        'Parti Federaliste': " = [[Parti fédéraliste (France)|PF]]",
        'Parti Fédéraliste Européen': " = [[Parti fédéraliste (France)|PF]]",
        'Regions Et Peuples Solidaires': " = [[Solidarité et progrès|SP]]",
        'Solidarité Et Progrès': " = [[Solidarité et progrès|SP]]",
        'Solidarite Et Progres': " = [[Solidarité et progrès|SP]]",
        'Parti Humaniste': " = [[Parti humaniste (France)|PH]]",
        'Parti Pour La Decroissance': " = [[Parti pour la décroissance|PD]]",
        'Rassemblement Des Contribuables Francais': " = [[Nicolas Miguet|Rassemblement des contribuables francais]]",
        'Parti Rachid Nekkaz': " = [[Rachid Nekkaz|Parti Rachid Nekkaz]]",
        'Parti Occitan':  " = [[Partit occitan|PO]]",
        'Gaulliste':  " = [[Gaullisme|Gaulliste]]",
        'Abertzaleen Batasuna':  " = [[Abertzaleen Batasuna|AB]]",
        'Parti Breton':  " = [[Parti breton|PB]]",
        'Energies Democrates': " = [[Christian Blanc|Energies democrates]]",
        "Udf - Mouvement Democrate": " = [[Union pour la démocratie française|UDF]]-[[Mouvement démocrate (France)|MODEM]]",
        'Union Pour La Raison Au Pouvoir': " = {{abréviation|URP|Union pour la Raison au Pouvoir}}",
        'Partit Per Catalunya': " = {{abréviation|PC|Partit Per Catalunya}}",
        'Centre Independant': " = {{abréviation|CI|Centre Indépendant}}",
        'Collectif Des Democrates Handicapes': " = {{abréviation|CDH|Collectif des Démocrates Handicapés}}",
        'Yvelines Ecologie': " = {{abréviation|YE|Yvelines Ecologie}}",
        'Sos Papa': " = {{abréviation|SP|Sos Papa}}",
        'La France De Demain': " = {{abréviation|FD|La France de demain}}",
        'Force Libertes': " = {{abréviation|FL|Force Libertés}}",
        'S.O.S. Papa': " = {{abréviation|SP|Sos Papa}}",
        'M.I.G.U.E.T. Maintenant !': " = {{abréviation|M.I.G.U.E.T|M.I.G.U.E.T. Maintenant !}}",
        "Ensemble Aujourd'Hui Mouvement Politique Des Droits Civiques": " = {{abréviation|EAMPDC|Ensemble aujourd'hui mouvement politique des droits civiques}}",
        'Mouvement Democrate': " = {{abréviation|MD|Mouvement Démocrate}}",
        'Ligue Socialiste Des Travailleurs': " = {{abréviation|LST|Ligue Socialiste des Travailleurs}}",
        "Vraie Liberte D'Expression": " = {{abréviation|VLE|Vraie Liberté d'Expression}}",
        'Alliance Reformatrice': " = {{abréviation|AR|Alliance Réformatrice}}",
        'Union Des Independants': " = {{abréviation|UI|Union des indépendants}}",
        "L'Enfant Et Son Droit": " = {{abréviation|ED|L'enfant et son droit}}",
        'Moment D’Agir': " = {{abréviation|MA|Moment d'agir}}",
        'Democratie Locale': " = {{abréviation|DL|Démocratie Locale}}",
        'Moins D Impot Gerer Utilement L Emploi P': " = {{abréviation|MIGUE|Moins d'impot gérer utilement l'emploi}}",
        'Front Liberation Des Oisifs Proletariens': " = {{abréviation|FLOP|Front libération des oisifs prolétariens}}",
        'Union Elargie Des Seniors': " = {{abréviation|UES|Union élargie des séniors}}",
        'Parti Des Musulmans De France': " = {{abréviation|PMF|Parti des musulmans de France}}",
        'Democrate Europeen': " = {{abréviation|DE|Démocrate Européen}}",
        'C.E.S.P.R.I.M.E.R  Autrement': " = {{abréviation|CESPRIMERA|C.E.S.P.R.I.M.E.R  Autrement}}",
        'Candidat De Marne Ecologie': " = {{abréviation|ME|Marne Ecologie}}",
        'Nationalforum Elsab-Lothringen Unabhã„Gig': " = {{abréviation|NEU|Nationalforum Elsab-Lothringen Unabhã„Gig}}",
        "Politique D'Action Citoyenne,Solidarite,": " = {{abréviation|PACS|Politique d'action citoyenne, solidarité}}",
        'Ecologie Nouvelle': " = {{abréviation|EN|Ecologie Nouvelle}}",
        "Union Des Victimes De L'Etat": " = {{abréviation|UVE|Union des Victimes de l'Etat}}",
        'Union Des Retraites Et Independants': " = {{abréviation|URI|Union des Retraites et Indépendants}}",
        'Des Animaux Et Mouvement Universaliste': " = {{abréviation|AMU|Des animaux et mouvement universaliste}}",
        'Non Communique': " = {{abréviation|NC|Non Communique}}",
        'Democratie Et Legitimite': " = {{abréviation|DL|Démocratie et Légitimité}}",
        'Association Victimes Ciments Francais': " = {{abréviation|AVCF|Association Victimes Ciments Français}}",
        'Parti Marginal Francais': " = {{abréviation|MF|Parti Marginal Français}}",
        'Ecologie Pluraliste Independante': " = {{abréviation|EPI|Ecologie Pluraliste Indépendante}}",
        'Groupement Politique Energies Democrates': " = {{abréviation|GPED|Groupement Politique Energies Démocrates}}",
        "Renouveau De L'Assemblee Nationale": " = {{abréviation|RAN|Renouveau de l'assemblée nationale}}",
        'Ecologie Independante': " = {{abréviation|EI|Ecologie Indépendante}}",
        'Ras Le Bol': " = {{abréviation|RB|Ras le bol}}",
        'Mouvement Social Democrate': " = {{abréviation|MSD|Mouvement Social Démocrate}}",
        'Ami Public': " = {{abréviation|AP|Ami Public}}",
        'Parti Du Ras Le Bol': " = {{abréviation|RB|Ras le bol}}",
        'Mouvement Ras Le Bol': " = {{abréviation|RB|Ras le bol}}",
        'Organisation Contre Le Systeme Ena': " = {{abréviation|OSENA|Organisation contre le systeme ENA}}",
        'Sos Syndic': " = {{abréviation|SS|Sos Syndic}}",
        'Pour La Verite Et La Justice Des Scandales Du Sieds Et De La Regie Du Sieds': " = {{abréviation|SIEDS|Pour la vérité et la justice des scandales du Sieds et de la régie du Sieds}}",
        'France Humaniste Et Visionniste': " = {{abréviation|FHV|France Humaniste et Visionniste}}",
        "Candidat De L'Union Nationale Ecologiste": " = {{abréviation|UNE|Union Nationale Ecologiste}}",
        "Stop A L'Autoroute": " = {{abréviation|SA|Stop à l'autoroute}}",
        "Defense Des Animaux Et Collectif National Defense Animale": " = {{abréviation|DACNDA|Défense des animaux et collectif national défense animale}}",
        "Candidate Du Parti Pour La Defense Des Animaux": " = {{abréviation|PDA|Parti pour la défense des animaux}}",
        "Solidarité Liberté Justice Paix": " = {{abréviation|SLJP|Solidarité Liberté Justice Paix}}",
        'Parti Pour La Defense Des Animaux Et Mouvement Universaliste': " = {{abréviation|AMU|Des animaux et mouvement universaliste}}",
        'Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste': " = {{abréviation|AMU|Des animaux et mouvement universaliste}}",
        'Parti Pour La Defense Des Animaux': " = {{abréviation|PDA|Parti pour la défense des animaux}}",
        'Developpement Social Democratie De Proximite': " = {{abréviation|DSDP|Développement Social Démocratie de Proximité}}",
        'Parti Des Socioprofessionnels': " = {{abréviation|PS|Parti des socioprofessionnels}}",
        'Mouvement Pour Une Citoyennete Republicaine': " = {{abréviation|MCR|Mouvement pour une Citoyenneté Républicaine}}",
        "Parti D'En Rire": " = {{abréviation|PR|Parti d'en Rire}}",
        "Union Ecologiste Et Democratie": " = {{abréviation|UED|Union Ecologiste et Démocratie}}",
        "Independant": " = {{abréviation|IND|Independant}}",
        'Mouvement Regionaliste De Bretagne': " = {{abréviation|MRB|Mouvement Régionaliste De Bretagne}}",
        "Rassemblement Pour L'Initiative Citoyenne": " = {{abréviation|RIC|Rassemblement pour l'initiative citoyenne}}",
        "Rassemblement Pour Initiative Citoyenne": " = {{abréviation|RIC|Rassemblement pour l'initiative citoyenne}}",
        "Rassemblement Des Savoisiens": " = {{abréviation|RS|Rassemblement des savoisiens}}",
        "Gip - Democratie Active": " = {{abréviation|GIP|GIP - Démocratie active}}",
        "La France En Action": " = {{abréviation|FA|La France en action}}",
        "Le Parti De L'Alliance": " = {{abréviation|PA|Le parti de l'alliance}}",
        'Union Nationale Ecologiste Sans Emploi': " = {{abréviation|UNESE|Union nationale écologiste sans emploi}}",
        "Parti Des Droits De L'Homme": " = {{abréviation|PDH|Parti des droits de l'Homme}}",
        "Solidaires Regions Ecologie": " = {{abréviation|SRE|Solidaires régions écologie}}",
        "Vam (Voter Am)": " = VAM",
        "Union Des Citoyens Independants": " = {{abréviation|UCI|Union des citoyens independants}}",
        "Union Des Citoyens Independants": " = {{abréviation|UCI|Union des citoyens independants}}",
        "Union Ecologie Et Democratie": " = {{abréviation|UED|Union Ecologie et Démocratie}}",
        "Mouvement Union Ecologie Et Democratie": " = {{abréviation|MUED|Mouvement Union Ecologie et Démocratie}}",
        "Divers": " = {{abréviation|DIV|Divers}}",
        "Union Pour L'Ecologie Et La Democratie": " = {{abréviation|UED|Union pour l'écologie et la démocratie}}",
        "Force De Rassemblement Republicaine Pour Une Citoyennete Plus Egale": " = {{abréviation|FRRCE|Force de Rassemblement Republicaine pour une citoyennete plus égale}}",
        "Gard Fraternite": " = {{abréviation|GF|Gard Fraternité}}",
        "Parti Du Vote Blanc": " = {{abréviation|PVB|Parti du vote blanc}}",
        "Ligue Savoisienne": " = {{abréviation|LS|Ligue Savoisienne}}",
        "Priorite Democratie En France": " = {{abréviation|PDF|Priorité démocratie en France}}",
        "Pour Respect Droits Acquis Pour Savoie": " = {{abréviation|RDAS|Pour respect droits acquis pour Savoie}}",
        "Parti Pirate": " = [[Parti pirate (France)|PR]]",
        "Parti De La Nation Occitane": " = [[Parti de la nation occitane|PNO]]",
        "Rassemblement Populaire Local": " = {{abréviation|RPL|Rassemblement populaire local}}",
        "Reseau Nouvelle Donne": " = [[Nouvelle Donne (parti politique)|ND]]",
        "Concordat Citoyen": " = {{abréviation|CC|Concordat citoyen}}",
        "Candidat Parachute": " = {{abréviation|CP|Candidat Parachute}}",
        "Union Royaliste": " = {{abréviation|UR|Union Royaliste}}",
        "Independant, Apolitique": " = {{abréviation|IA|Indépendant, Apolitique}}",
        "Convergence Ecologie Solidarite": " = {{abréviation|CES|Convergence écologie solidarité}}",
        "Parti Blanc": " = {{abréviation|PB|Parti blanc}}","Parti Blanc": " = {{abréviation|PB|Parti blanc}}",
        "Ordre Republicain Francais": " = {{abréviation|ORF|Ordre républicain français}}",
        "Solidarite Ecologie Gauche Alternative": " = {{abréviation|SEGA|Solidarite Ecologie Gauche Alternative}}",
        "Reformes, Democratie Sante": " = {{abréviation|ORF|Réformes, démocratie santé}}",
        "Entreprise Emplois": " = {{abréviation|EE|Entreprise emplois}}",
        "Alliance Pour L'Ecologie Et La Democratie": " = {{abréviation|AED|Alliance pour l'écologie et la démocratie}}",
        "Droit De Chasse": " = {{abréviation|DC|Droit de chasse}}",
        "Pour Les Droits D'Auteurs": " = {{abréviation|DA|Pour les droits d'auteurs}}",
        "Union Des Ecologistes": " = {{abréviation|UE|Union des écologistes}}",
        "Parti Ras Le Bol": " = {{abréviation|PRB|Parti ras le bol}}",
        "L'Union Nationale Ecologiste Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = {{abréviation|UNE|Union Nationale Ecologiste}}-{{abréviation|PD|Parti pour la Défense}}-{{abréviation|MU|Mouvement Universaliste}}",
        "Union Nationale Ecologiste Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = {{abréviation|UNE|Union Nationale Ecologiste}}-{{abréviation|PD|Parti pour la Défense}}-{{abréviation|MU|Mouvement Universaliste}}",
        "Union Nationale Ecologiste, Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = {{abréviation|UNE|Union Nationale Ecologiste}}-{{abréviation|PD|Parti pour la Défense}}-{{abréviation|MU|Mouvement Universaliste}}",
        "Union Nationale Ecologiste, Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = {{abréviation|UNE|Union Nationale Ecologiste}}-{{abréviation|PD|Parti pour la Défense}}-{{abréviation|MU|Mouvement Universaliste}}",
        "Union Nationale Ecologiste, Parti Pour La Defense Des Animaux Et Mouvement Universaliste": " = {{abréviation|UNE|Union Nationale Ecologiste}}-{{abréviation|PD|Parti pour la Défense}}-{{abréviation|MU|Mouvement Universaliste}}",
        "Union Nationale Ecologie, Parti Pour La Defense Des Animaux Et Mouvement Universaliste": " = {{abréviation|UNE|Union Nationale Ecologiste}}-{{abréviation|PD|Parti pour la Défense}}-{{abréviation|MU|Mouvement Universaliste}}",
        "Union Nationale Ecologiste": " = {{abréviation|UNE|Union Nationale Écologiste}}",
        "Candidate De L'Union Nationale Ecologiste": " = {{abréviation|UNE|Union Nationale Écologiste}}",
        "Ecologie Alternative Autogestion": " = {{abréviation|EAA|Écologie alternative autogestion}}",
        "Rassemblement Des Democrates Et Des Republicains De Progres": " = {{abréviation|RDRP|Rassemblement des démocrate et des républicains de progrès}}",
        "Rassemblement Des Democrate Et Des Republicains De Progres": " = {{abréviation|RDRP|Rassemblement des démocrate et des républicains de progrès}}",
        "Le Parti De L'Arbre Pour La Sante De La Terre Des Hommes Et Des Generations Futures": " = {{abréviation|PASTHGF|le Parti de l'Arbre pour la Santé de la Terre des Hommes et des Générations Futures}}",
        "Union Democratique Bretonne": " = [[Union démocratique bretonne|UDB]]",
        "Parti De La Loi Naturelle (Pln)": " = [[Parti de la loi naturelle|PLN]]"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_extremedroite(argument, order_number):
    switcher = {
        'empty': " = [[Extrême droite en France|EXD]]",
        'Extreme Droite': " = [[Extrême droite en France|EXD]]",
        'Candidature Personnelle D Extreme Droite': " = [[Extrême droite en France|EXD]]",
        "Mnr - Contre L'Immigration-Islamisation, L'Insecurite": " = [[Mouvement national républicain|MNR]]",
        "Mnr - Contre L'Immigration-Islamisation": " = [[Mouvement national républicain|MNR]]",
        'Mouvement National Republicain': " = [[Mouvement national républicain|MNR]]",
        'Union De La Droite Nationale': " = [[Union de la droite nationale|UDN]]",
        'Parti Anti-Sioniste': " = [[Parti antisioniste|PAS]]",
        'Defendons La Chasse Et Nos Traditions': " = {{abréviation|DCT|Défendons la chasse et nos traditions}}",
        'Rassemblement Republicain Pour L Union Centriste': " = {{abréviation|RRUC|Rassemblement républicain pour l'union centriste}}",
        'Candidat Du Rassemblement Des Democrates Et Des Republicains De Progres': " = {{abréviation|RDRP|Rassemblement des Démocrates et des Républicains de Progrés}}",
        'Candidate Du Rassemblement Des Democrates Et Des Republicains De Progres': " = {{abréviation|RDRP|Rassemblement des Démocrates et des Républicains de Progrés}}",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Jeune Bretagne': " = [[Jeune Bretagne|JB]]",
        'Bloc Identitaire': " = [[Les Identitaires|BI]]",
        'Alliance Populaire': " = {{abréviation|AP|Alliance Populaire}}",
        'Mouvement De Rassemblement National': " = {{abréviation|MRN|Mouvement de Rassemblement National}}",
        'Mouvement De Rassemblement National Alliance Populaire': " = {{abréviation|MRNAP|Mouvement de Rassemblement National Alliance Populaire}}",
        "Alsace Debout Contre L'Insecurite Et L'Immigration": " = {{abréviation|ADII|Alsace debout contre l'insécurité et l'immigration}}",
        'Parti National Radical': " = {{abréviation|PNR|Parti National Radical}}",
        'Front Francais': " = {{abréviation|FF|Front Français}}",
        "Les Francais D'Abord": " = {{abréviation|FA|Les Français d'Abord}}",
        "Trop D'Immigres, La France Aux Francais": " = {{abréviation|IFF|Trop d'immigrés, la France aux Francais}}",
        "Trop D Immigres La France Aux Francais": " = {{abréviation|IFF|Trop d'immigrés, la France aux Francais}}",
        'Alternative Nationale': " = {{abréviation|AN|Alternative Nationale}}",
        'Savoie Independante': " = {{abréviation|SI|Savoie Indépendante}}",
        'Nouvelle Solidarite': " = {{abréviation|NS|Nouvelle Solidarité}}",
        'Parti National Republicain': " = {{abréviation|PNR|Parti national républicain}}",
        'Parti Ouvrier Europeen': " = [[Parti ouvrier européen|POE]]",
        'Parti Ouvrier Europeen': " = [[Parti ouvrier européen|POE]]",
        'Parit Ouvrier Europeen': " = [[Parti ouvrier européen|POE]]",
        'Solidarite Et Progres': " = {{abréviation|SP|Solidarité et Progrès}}",
        'Union Des Independants': " = {{abréviation|UI|Union des indépendants}}",
        'Mouvement Travail Patrie': " = {{abréviation|MTP|Mouvement Travail Patrie}}",
        "Universelle Fondation Drogues, Crimes Contre L'Humanite": " = {{abréviation|UFDCCH|Universelle Fondation Drogues, Crimes Contre L'Humanite}}",
        'Alliance Populaire, Mouvement De Rassemblement National': " = {{abréviation|AP|Alliance populaire}} - {{abréviation|MRN|Mouvement de rassemblement national}}",
        'Alliance Populaire, Rassemblement Des Forces Nationales': " = {{abréviation|AP|Alliance populaire}} - {{abréviation|MRN|Mouvement de rassemblement national}}",
        "Candidate De L'Alliance Populaire": " = {{abréviation|AP|Alliance populaire}}",
        "Rassemblement Des Democrates Et Des Republicains De Progres": " = {{abréviation|RDRP|Rassemblement des démocrates et des républicains de progrès}}",
        "Rassemblement Des Democrates Et Des Republicains Des Progres": " = {{abréviation|RDRP|Rassemblement des démocrates et des républicains de progrès}}",
        "Rassemblement Des Forces Nationales Presente Par L'Alliance Populaire": " = {{abréviation|RFNAP|Rassemblement des forces nationales présenté par l'alliance populaire}}",
        "Parti De La Loi Naturelle": " = [[Parti de la loi naturelle|PLN]]",
        "Parti Pour La Loi Naturelle": " = [[Parti de la loi naturelle|PLN]]",
        "Candidat De L'Alliance Populaire": " = {{abréviation|AP|Alliance populaire}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_ecologiste(argument, order_number):
    switcher = {
        'Ecologiste': " = [[Écologisme|ECO]]",
        'Autre Ecologiste': " = [[Écologisme|ECO]]",
        'empty': " = [[Écologisme|ECO]]",
        'Génération Écologie': " = [[Génération écologie|GE]]",
        'Generation Ecologie': " = [[Génération écologie|GE]]",
        'Les Verts': " = [[Les Verts (France)|LV]]",
        'Les Verts Soutien Parti Socialiste': " = [[Les Verts (France)|LV]]-[[Parti socialiste (France)|PS]]",
        'Rassemblement La Gauche Avec Les Verts': " = [[Les Verts (France)|LV]]",
        'Ecologie Les Verts': " = [[Les Verts (France)|LV]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Europe-Ecologie-Les Verts': " = [[Europe Écologie Les Verts|EELV]]",
        'Europe-Ecologie-Les Verts (Soutien Ps)': " = [[Europe Écologie Les Verts|EELV]]-[[Parti socialiste (France)|PS]]",
        'Alliance Ecologiste Indépendante': " = [[Alliance écologiste indépendante|AEI]]",
        'Le Trefle': " = [[Le Trèfle - Les nouveaux écologistes|Le Trèfle]]",
        'Le Trèfle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|Le Trèfle]]",
        'Le Trefle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|Le Trèfle]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecologistes Hommes Nature Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Mouvement Écologiste Indépendant': " = [[Mouvement écologiste indépendant|MEI]]",
        'Mouvement Ecologiste Independant': " = [[Mouvement écologiste indépendant|MEI]]",
        'Mouvement Hommes Animaux Nature': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Homme Nature Animaux': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Hommes-Animaux-Nature : Mhan': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Des Ecologistes Independants': " = [[Mouvement écologiste indépendant|MEI]]",
        'Cap 21': " = [[Cap21]]",
        'Citoyennete Action Pour Le 21E Siecle': " = [[Cap21]]",
        'Citoyennete Action Participation Pour Le 21E Siecle': " = [[Cap21]]",
        'Une France Humaine': " = {{abréviation|FH|Une France Humaine}}",
        'Union Des Ecologistes En Seine Maritime': " = {{abréviation|UESM|Union des Ecologistes en Seine Maritime}}",
        'Ecologie Pour L Alsace Du Nord': " = {{abréviation|FH|Écologie pour l'Alsace du nord}}",
        'Ecologie Artisanale': " = {{abréviation|EA|Écologie Artisanale}}",
        'Ecologie Nature Environnement': " = {{abréviation|ENE|Ecologie Nature Environnement}}",
        'Verts Alternatifs': " = {{abréviation|VA|Verts Alternatifs}}",
        'Verte Alternative': " = {{abréviation|VA|Verts Alternatifs}}",
        'Parti Vert': " = {{abréviation|PV|Parti Vert}}",
        'Pour Une Alternative Ecologiste, Citoyenne Et Progressiste': " = {{abréviation|AECP|Pour une Alternative Ecologiste, Citoyenne et Progressiste}}",
        'Republique Ecologie Democratie': " = {{abréviation|RED|République Ecologie Démocratie}}",
        'Ecologie Et Democratie': " = {{abréviation|ED|Ecologie et démocratie}}",
        'Anjou Ecologie Autogestion': " = {{abréviation|AEA|Anjou Ecologie Autogestion}}",
        'Union Nationale Ecologiste': " = {{abréviation|UNE|Union nationale écologiste}}",
        'Anjou Ecologie Autogestion': " = {{abréviation|AEA|Anjou Écologie Autogestion}}",
        'Vivre Ensemble Dans Une Meuse Propre': " = {{abréviation|VEMP|Vivre ensemble dans une Meuse propre}}",
        'Les Ecologistes Regionalistes Solidaires Et Citoyens': " = {{abréviation|ERSC|Les Écologistes Régionalistes Solidaires et Citoyens}}",
        'Ecologie Et Citoyens': " = {{abréviation|EC|Ecologie et citoyens}}",
        'Eden-Republique Et Democratie': " = {{abréviation|EDEN-RD|Eden-République et démocratie}}",
        'Ecologiste Independant': " = {{abréviation|EI|Ecologiste indépendant}}",
        'Parti Ecologiste': " = [[Parti écologiste|PE]]",
        'Renouveau Ecologique': " = {{abréviation|RE|Renouveau écologique}}",
        'Paris Oxygene': " = {{abréviation|PO|Paris Oxygène}}",
        'Nouveaux Ecologistes': " = {{abréviation|NE|Nouveaux écologistes}}",
        'Confederation Des Ecologistes Independants': " = {{abréviation|CEI|Confédération des écologistes indépendants}}",
        'Souverainete Ecologie Ruralite': " = {{abréviation|SER|Souveraineté écologie ruralité}}",
        'Ecologie Et Citoyens-Solidaires-Regions-Ecologie': " = {{abréviation|ECSRE|Ecologie et Citoyens-Solidaires-Régions-Ecologie}}",
        'Parti Pour La Defense Des Animaux': " = {{abréviation|DA|Parti pour la défense des animaux}}",
        'Ensemble, Ecologistes Et Solidaires': " = {{abréviation|EES|Ensemble, Écologistes et Solidaires}}",
        "Candidat Libre Pour Le Respect De L'Electeur": " = {{abréviation|CLRE|Candidat libre pour le respect de l'électeur}}",
        'Solidarite Ecologie Gauche Alternative': " = [[Les Alternatifs|SEGA]]",
        'Parti De L Entente': " = {{abréviation|PE|Parti de l'entente}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_communiste(argument, order_number):
    switcher = {
        'empty': " = [[Communisme|COM]]",
        'Communistes': " = [[Communisme|COM]]",
        'Communiste': " = [[Communisme|COM]]",
        'Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Partie Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Parti Comâ­Muniste Francais': " = [[Parti communiste français|PCF]]",
        'Parti Commuâ­Niste Francais': " = [[Parti communiste français|PCF]]",
        'Forces De Gauche Pcf': " = [[Parti communiste français|PCF]]",
        'Candidate De Rassemblement Des Forces De Gauche Presentee Par Le P C F': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Presente Par Le Parti Comâ­Muniste Francais': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Presente Par Le Pcf': " = [[Parti communiste français|PCF]]",
        'Rassemblement Des Forces De Gauche Presente Par Le P C F': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Des Forces De Gauche Presente Par Le Pcf': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Des Forces De Gauche Presente Par Le P C F': " = [[Parti communiste français|PCF]]",
        'Candidat De Ressemblement Des Forces De Gauche Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Des Forces De Progres Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Pour Se Defendre Et Faire Du Neuf Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Rassemblement Pour Se Defendre Et Faire Du Neuf Presentee Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Rassemblement Pour Se Defendre Et Faire Du Neuf Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Rassemblement Des Forces De Gauche Presente Par Le Pcf': " = [[Parti communiste français|PCF]]",
        'Rassemblement Des Forces De Gauche Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Parti Communiste Francais Pour Le Rassemblement Des Forces Progressistes Et Le Changement': " = [[Parti communiste français|PCF]]",
        'Parti Communiste Francais, Pour Le Rassemblement Des Forces Progressistes Et Le Changement': " = [[Parti communiste français|PCF]]",
        'Parti Communiste': " = [[Parti communiste français|PCF]]",
        'Rassemblement Gauche Unie Et Anti Liberale': " = [[Gauche antilibérale|RGUAL]]",
        'Gauche Antiliberale': " = [[Gauche antilibérale|GA]]",
        'Candidat Rassemblement Pcf': " = [[Parti communiste français|PCF]]",
        'Gauche Alternative Et Antiliberale': " = [[Gauche antilibérale|GA]]",
        'Rassemblement Des Forces De Gauche': " = {{abréviation|RFG|Rassemblement des forces de gauche}}",
        'Mouvement Refondations': " = {{abréviation|MR|Mouvement Refondations}}",
        'Candidat Du Rassemblement Et Des Forces De Progres': " = {{abréviation|RFP|Rassemblement et des forces de progrès}}",
        'Candidate Du Rassemblement Et Des Forces De Progres': " = {{abréviation|RFP|Rassemblement et des forces de progrès}}",
        'Gauche Populaire Et Antiliberale Soutenue Par Pcf': " = {{abréviation|GPA|Gauche populaire et antilibérale - PCF}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

url = 'https://query.wikidata.org/sparql'
query = """
SELECT DISTINCT ?itemLabel ?sitelink WHERE {
  ?item wdt:P27 wd:Q142;
        wdt:P31 wd:Q5;
        wdt:P106 wd:Q82955;
        wdt:P569 ?age;
  FILTER(YEAR(?age) >= 1858).
  ?article schema:name ?sitelink ;
           schema:about ?item ;
           schema:isPartOf <https://fr.wikipedia.org/> .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
}
"""
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()

candidat_list = {}

for i in range(0,len(data['results']['bindings'])):
  candidat_list[remove_accents(data['results']['bindings'][i]['itemLabel']['value'])] = data['results']['bindings'][i]['sitelink']['value']

sys.argv = ['circo.py', '-d', "VAUCLUSE", '-c', '5']
#on recupere les options utilisateurs
parser = argparse.ArgumentParser(description="Gap filling programms")
#recupere le fichier comportant les reads
parser.add_argument("-d", "--departement", required=True)
#recupere le fichier comportant le start et stop
parser.add_argument("-c", "--circo", required=True, type=int)
param = parser.parse_args()

election(1958, "23 et 30 novembre", "23/11/1958", param.departement, param.circo)
election(1962, "18 et 25 novembre", "18/11/1962", param.departement, param.circo)
election(1967, "5 et 12 mars", "05/03/1967", param.departement, param.circo)
election(1968, "23 et 30 juin", "23/06/1968", param.departement, param.circo)
election(1973, "4 et 11 mars", "11/03/1973", param.departement, param.circo)
election(1978, "12 et 18 mars", "12/03/1978", param.departement, param.circo)
election(1981, "14 et 21 juin", "14/06/1981", param.departement, param.circo)
election(1988, "5 et 12 juin", "05/06/1988", param.departement, param.circo)
election(1993, "12 et 21 mars", "21/03/1993", param.departement, param.circo)
election(1997, "12 et 21 mars", "21/03/1997", param.departement, param.circo)
election(2002, "9 et 12 juin", "09/06/2002", param.departement, param.circo)
election(2007, "10 et 12 juin", "10/06/2007", param.departement, param.circo)
election(2012, "10 et 17 juin", "10/06/2012", param.departement, param.circo)