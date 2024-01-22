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
            if v != [0, 0]:
                print("| candidat", i," = Inconnu", sep = '')
                partie_name(k, i)
                print("| suffrages", i, " = ", v[0], sep = '')
                couleur_hex(k, i)
                i += 1
        print("}}")

def corps_post(premier_tour):
    dicovoix = {}
    for index, row in premier_tour.iterrows():
        u = 1
        print(index)
        check = 0
        while type(check) != float:
            nuance = str(u) + ' nuance'
            prenom = str(u) + ' Prénom candidat'
            nom = str(u) + ' Nom candidat'
            voix = str(u) + ' voix'
            label = str(u) + ' Etiquette liste'
            acces = str(u) + 'Accès second tour'
            print(row[label].title())
            pname = partie_name_post(row[nuance], row[label].title())
            print(pname)
            #verifie l existence d'un candidat supplementaire
            u += 1
            label = str(u) + ' Etiquette liste'
            if label in row.index:
                #verifie l existence d'un candidat supplementaire
                check = row[label]
            else:
                check = 0.5






def test():

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
            if row[nom] + " " + row[prenom] in wikidata_name.keys():
                #si le nom de page different
                if row[nom] + " " + row[prenom] != wikidata_name[row[nom] + " " + row[prenom]]:
                    #si le nom de page different
                    if row[nom] + " " + row[prenom] != remove_accents(wikidata_name[row[nom] + " " + row[prenom]]):
                        print("| candidat", i, " = [[", wikidata_name[row[nom] + " " + row[prenom]], "|", diconom[k][0], " ", diconom[k][1], "]]", sep = '')
                    #si probleme d'accent
                    else:
                        print("| candidat", i, " = [[", wikidata_name [row[nom] + " " + row[prenom]], "]]", sep = '')
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
            if row[nom] + " " + row[prenom] in wikidata_name.keys():
                #si le nom de page different
                if row[nom] + " " + row[prenom] != wikidata_name[row[nom] + " " + row[prenom]]:
                    #si le nom de page different
                    if row[nom] + " " + row[prenom] != remove_accents(wikidata_name[row[nom] + " " + row[prenom]]):
                        print("| candidat", i, " = [[", wikidata_name[row[nom] + " " + row[prenom]], "|", diconom[k][0], " ", diconom[k][1], "]]", sep = '')
                    #si probleme d'accent
                    else:
                        print("| candidat", i, " = [[", wikidata_name [row[nom] + " " + row[prenom]], "]]", sep = '')
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

def couleur_hex(argument):
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

def print_hex(argument):
    return "| hex" + str(order_number) + argument

def switch_hex_recent(argument, dictionary, order_number):
    switcher = {
        'FDG': print_hex(" = {{Infobox Parti politique français/couleurs|-FG}}"),
        'UMP': print_hex(" = {{Infobox Parti politique français/couleurs|-UMP}}"),
        'SOC': print_hex(" = {{Infobox Parti politique français/couleurs|-SOC}}"),
        'PRG': print_hex(" = {{Infobox Parti politique français/couleurs|-PRG}}"),
        'RDG': print_hex(" = {{Infobox Parti politique français/couleurs|-PRG}}"),
        'RPR': print_hex(" = {{Infobox Parti politique français/couleurs|-RPR}}"),
        'UDF': print_hex(" = {{Infobox Parti politique français/couleurs|-UDF}}"),
        'GEC': print_hex(" = {{Infobox Parti politique français/couleurs|-GE}}"),
        'SDC': print_hex(" = {{Infobox Parti politique français/couleurs|-PS}}"),
        'VEC': print_hex(" = {{Infobox Parti politique français/couleurs|-Verts}}"),
        'FRN': print_hex(" = {{Infobox Parti politique français/couleurs|-FN}}"),
        'MAJ': print_hex(" = {{Infobox Parti politique français/couleurs|-DIV}}"),
        'ECI': print_hex(" = {{Infobox Parti politique français/couleurs|-DIV}}"),
        'PRV': print_hex(" = {{Infobox Parti politique français/couleurs|-PR}}"),
        'REG': print_hex(" = {{Infobox Parti politique français/couleurs|-REG}}"),
        'EXO': print_hex(" = {{Infobox Parti politique français/couleurs|-EXD}}"),
        'EXG': switch_extremegauche_hex(etiquette),
        'DVD': switch_diversdroite_hex(etiquette),
        'DVG': switch_diversgauche_hex(etiquette),
        'DIV': switch_divers_hex(etiquette),
        'EXD': switch_extremedroite_hex(etiquette),
        'ECO': switch_ecologiste_hex(etiquette),
        'COM': print_hex(" = {{Infobox Parti politique français/couleurs|-COM}}", order_number)
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument[:3], lambda: "error")
    # Execute the function
    print(func)

def switch_extremegauche_hex(argument):
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

def switch_diversdroite_hex(argument):
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

def switch_diversgauche_hex(argument):
    switcher = {
        'Socialiste Dissidente': " = {{Infobox Parti politique français/couleurs|-PS}}",
        'empty': " = {{Infobox Parti politique français/couleurs|-DVG}}",
        'Mouvement Des Citoyens': " = {{Infobox Parti politique français/couleurs|-MDC}}",
        'Energie Radicale': " = {{Infobox Parti politique français/couleurs|-PRG}}",
        'Mouvement Républicain Et Citoyen': " = {{Infobox Parti politique français/couleurs|-MRC}}",
        'Parti Socialiste': " = {{Infobox Parti politique français/couleurs|-PS}}",
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-DVG}}"), order_number)

def switch_divers_hex(argument):
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

def switch_extremedroite_hex(argument):
    switcher = {
        'Mouvement National Republicain': " = {{Infobox Parti politique français/couleurs|-MNR}}",
        "Mnr - Contre L'Immigration-Islamisation, L'Insecurite": " = {{Infobox Parti politique français/couleurs|-MNR}}",
        "Mnr - Contre L'Immigration-Islamisation": " = {{Infobox Parti politique français/couleurs|-MNR}}",
        'Mouvement National Republicain': " = {{Infobox Parti politique français/couleurs|-MNR}}",
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-EXD}}"), order_number)

def switch_ecologiste_hex(argument):
    switcher = {
        'Generation Ecologie': " = {{Infobox Parti politique français/couleurs|-GE}}",
        'Les Verts': " = {{Infobox Parti politique français/couleurs|-Verts}}",
        'Europe-Ecologie-Les Verts': " = {{Infobox Parti politique français/couleurs|-EELV}}",
        'Alliance Ecologiste Indépendante': " = {{Infobox Parti politique français/couleurs|-AEI}}",
        'Mouvement Ecologiste Independant': " = {{Infobox Parti politique français/couleurs|-MEI}}",
        'Mouvement Écologiste Indépendant': " = {{Infobox Parti politique français/couleurs|-MEI}}"
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-ECO}}"), order_number)

def partie_name(argument):
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
    print(print(switcher.get(argument, " =  error"), order_number))

def partie_name_post(nuance, etiquette):
    if nuance[:5] == 'MODEM':
        return 'MODEM'
    elif nuance[:5] == 'NouvC':
        return 'LC'
        print(" = [[Les Centristes|LC]]")
    elif nuance[:4] == 'PSLE':
        return 'LC'
    else:
        switch_partie_recent(nuance, etiquette)

def switch_partie_recent(nuance, etiquette):
    switcher = {
        'ECI': "DIV",
        'PRV': "PRV",
        'MAJ': "MP",
        'FRN': "FN",
        'VEC': "LV",
        'GEC': "GE",
        'UDF': "UDF",
        'RPR': "RPR",
        'PRG': "PRG",
        'RDG': "PRG",
        'SOC': "PS",
        'SCO': "PS",
        'SDC': "PS",
        'UMP': "UMP",
        'FDG': "FDG",
    }
    return switcher.get(nuance[:3], switch_partie_recent_bis(nuance, etiquette))

def switch_partie_recent_bis(nuance, etiquette):
    if (nuance == 'EXO'):
        return switch_exocode(etiquette)
    elif (nuance == 'REG'):
        return switch_regionalisme(etiquette)
    elif (nuance == 'EXO'):
        return switch_exocode(etiquette)
    elif (nuance == 'EXG'):
        return switch_extremegauche(etiquette)
    elif (nuance == 'DVD'):
        return switch_diversdroite(etiquette)
    elif (nuance == 'DVG'):
        return switch_diversgauche(etiquette)
    elif (nuance == 'DIV'):
        return switch_divers(etiquette)
    elif (nuance == 'EXD'):
        return switch_extremedroite(etiquette)
    elif (nuance == 'ECO'):
        return switch_ecologiste(etiquette)
    elif (nuance == 'COM'):
        return switch_communiste(etiquette)
    else:
        return 'error'

def switch_exocode(argument):
    switcher = {
        'empty': " = Error",
        'Parti ouvrier européen': " = [[Parti ouvrier européen|POE]]"
    }
    return print(switcher.get(argument, " = " + argument))

def switch_regionalisme(argument):
    switcher = {
        'empty': "REG",
        'Unitat Catalana': "UC",
        'Abertzaleen Batasuna':  "AB",
        'Union Du Peuple Alsacien':  "UPA",
        'Abertzale Nationaliste Basque':  "AB",
        'Abertzale Nationaliste Basque':  "AB",
        "Alsace D'Abord, Pour L'Europe Des Regions":  "AA",
        "Alsace D'Abord":  "AA",
        'Erc (Esquarra Republicana Catalana)':  "GRC",
        "Ea Cusko Alkartasuna": "REG",
        "La Radio Des Alsaciens 107 4 Mhz": "REG",
        "Radio Alsaciens 107 4 Mhz": "REG",
        "Entente Des Ecologistes, Les Verts": "REG",
    }
    return print(switcher.get(argument, "Error : " + argument))

def switch_extremegauche(argument):
    switcher = {
        'empty': "EXG",
        'Lutte Ouvrière': "LO",
        'Lutte Ouvriere': "LO",
        'Alternative Democratie Socialisme': "ADS",
        'Candidat De Lutte Ouvriere': "LO",
        'Ligue Communiste Revolutionnaire': "LCR",
        'Ligue Communiste Revolutionnaire (Dissident)': "LCR",
        'Nouveau Parti Anticapitaliste': "NPA",
        'Alternatifs (Solidarite, Ecologie, Gauche Alternative)': "Alternatif",
        'Gauche Alternative Et Ecologiste': "Alternatif",
        'Les Alternatifs': "Alternatif",
        'Extreme Gauche': "EXG",
        'Extrême gauche': "EXG",
        'Parti Pour La Décroissance': "PPLD",
        'Parti Des Travailleurs': "PT",
        'Parti Des Travailâ­Leurs': "PT]]",
        'Mouvement De La Gauche Progressiste': "MGP",
        'Gauche Alternative 2007': "GP2007",
        'A Gauche Autrement, Sega (Solidarite, Ecologie, Gauche Alternative)': "GP2007",
        'Alternative Rouge Et Verte': "ARV",
        'Mouvement Pour Un Parti Des Travailleurs (Mppt)': "MPPT",
        'Sans Etiquette': "EXG",
        'Solidarite, Ecologie, Gauche Alternative (Sega)': "SEGA",
        'Solidarite Ecologie Gauche Alternative (Sega)': "SEGA",
        'Solidarite, Ecologie Gauche Alternative': "SEGA",
        'Solidarite Ecologie Gauche Alternative': "SEGA",
        "Mouvement Ecologiste De L'Anjou, Solidarite, Ecologie Gauche Alternative (Sega)": "SEGA",
        'Candidat D Initiative Pour Une Nouvelle Politique A Gauche': "EXG",
        'Voix Des Travailleurs': "VdT",
        'Les Alternatifs-Ecologie-Autogestion': "Alternatif",
        "Gauche Alternative 2012": "EXG",
        "A Gauche Autrement": "EXG",
        "Ligue Socialiste Des Travailleurs": "EXG",
        "Ecologie Pacifisme Objection De Croissance": "EXG",
        "Changer A Gauche": "EXG",
        "Comite Pour La Defense Du Regime Local": "EXG",
        "Tous Ensemble A Gauche": "EXG",
        "Collectif Antiliberal Du Pays De Lorient": "EXG",
        "100% A Gauche - Lcr": "LCR",
        "L.C.R. 100% A Gauche": "LCR",
        "Union Pour L'Ecologie Et La Democratie": "EXG",
        "Autogestion Soutenu Par Les Verts": "EXG",
        "Anjou Ecologie Autogestion": "EXG",
        "A Gauche Toute Collectif Pour Une Gauc": "EXG",
        "Pole Rennaissance Communiste En France": "PRCF",
        'Union Pour La Gauche Renovee': "EXG",
        'Initiative Pour Une Nouvelle Politique Gauche': "EXG",
        'Candidat D Initiative Pour Une Nouvelle Politique De Gauche': "EXG",
        'Tous Ensemble A Gauche': "EXG",
        "Parti Ouvrier Indépendant": "POI",
        'A Gauche Vraiment': "EXG",
        'Mouvement A Gauche Vraiment': "EXG",
        'Gauche Alternative': "EXG",
        'Parti Des Evidences Concretes': "EXG",
        'Pour Une Nouvelle Politique A Gauche': "EXG",
        'Rassemblement Utile A Tous': "EXG",
    }
    return switcher.get(argument, "Error: " + argument)

def switch_diversdroite(argument):
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
        'Centre National Des Independants Et Paysans': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Centre National Des Independants Et Paysans (Cni)': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Centre National Des Independants Et Paysans (Cnip)': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Cnip': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Centre National Des Independants': " = [[Centre national des indépendants et paysans|CNI]]",
        'Droite De Conviction Pour La Defense Des Valeurs Presente Par Le Centre National Des Independants Et Paysans Cni': " = {{abréviation|DCDV|Droite de conviction pour la défense des valeurs}}-[[Centre national des indépendants et paysans|CNI]]",
        'Droite De Conviction Pour La Defense Des Valeurs Presente Par Le Centre National Des Independants Et Paysans (Cni) Et La Democratie Chretienne Francaise (Dcf)': " = {{abréviation|DCDV|Droite de conviction pour la défense des valeurs}}-[[Centre national des indépendants et paysans|CNI]]-{{abréviation|DCF|Démocratie Chrétienne Française}}",
        'Parti Chrétien-Démocrate': " = [[VIA, la voie du peuple|PCD]]",
        'Union Républicaine Populaire': " = [[Union populaire républicaine (2007)|UPR]]",
        'Divers Droite': " = [[Divers droite|DVD]]",
        'Lyon Divers Droite (Soutien Pcd Et Mpf)': " = [[Divers droite|DVD]]",
        'Lyon Divers Droite': " = [[Divers droite|DVD]]",
        'La Droite Independante (Mpf)': " = [[La droite indépendante|LDI]]",
        'Rassemblement Pour La France': " = [[Rassemblement pour la France|RPF]]",
        'Union Des Démocrates Pour La République': " = [[Union des démocrates pour la République|UDR]]",
        'Rassemblement Pour La Republique': " = [[Rassemblement pour la République|RPR]]",
        "Union De L'Opposition Udf-Rpr": " = [[Union pour la démocratie française|UDF]]-[[Rassemblement pour la République|RPR]]",
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
        'Candidat Republicain Du Beaujolais': " = {{abréviation|CRB|Candidat républicain du Beaujolais}}",
        'Alliance Radicale Et Centriste': " = {{abréviation|ARC|Alliance radicale et centriste}}",
        'Objectif Decroissance': " = {{abréviation|OD|Objectif Décroissance}}",
        'Comite L Alsace Merite Mieux': " = {{abréviation|CAMM|Comite l'Alsace mérite mieux}}",
        'Rassemblement Des Democrates Et Des Republicains De Progres': " = {{abréviation|RDRP|Rassemblement des démocrates et des républicains de progrès}}",
        'Union Pour La Democratie Francaise Dissident': " = {{abréviation|UDFD|Union pour la démocratie française dissident}}",
        'Pour L Union Des Partis Politiques Francais': " = {{abréviation|UPPF|Pour l'union des partis politiques francais}}",
        'Federation Des Independants Du Bas Rhin Cin': " = {{abréviation|FIBR|Fédération des indépendants du Bas-Rhin}}",
        'Cand. Indept  Defense Du Monde Rural': " = {{abréviation|CIDMR|Candidat Indépendent défense du monde rural}}",
        'Union Centriste Republicaine': " = {{abréviation|UCR|Union Centriste Républicaine}}",
        "Ensemble, L'An 2000": " = {{abréviation|EA2000|Ensemble, l'an 2000}}",
        "Rassemblement Pour L'Independance De L'Europe": " = {{abréviation|RIE|Rassemblement pour l'indépendance de l'Europe}}",
        'Dvd Union De La Droite - Mp': " = {{abréviation|UD-MP|Union de la droite - MP}}",
        'Union Centriste': " = {{abréviation|UC|Union Centriste}}",
        'Rassemblement Des Independants': " = {{abréviation|RI|Rassemblement des indépendants}}",
        'Parti Blanc': " = {{abréviation|PB|Parti Blanc}}",
        "Independant D'Opposition": " = {{abréviation|IO|Indépendant d'opposition}}",
        "Union Royaliste": " = {{abréviation|UR|Union Royaliste}}",
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
        'Cap Liberte Egalite Fraternite': " = {{abréviation|CLEF|Cap Liberté Egalité Fraternité}}",
        'Union Du Rassemblement Et Du Centre': " = {{abréviation|URC|Union du rassemblement et du centre}}"
    }
    return print(switcher.get(argument, " = " + argument))

def switch_diversgauche(argument):
    switcher = {
        'Divers Gauche': " = [[Divers gauche|DVG]]",
        'empty': " = [[Divers gauche|DVG]]",
        'Pole Republicain': " = [[Pôle républicain|PR]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Mouvement Republicain Et Citoyen': " = [[Mouvement républicain et citoyen|MRC]]",
        'Socialiste Dissidente': " = [[Dissidence|diss]] [[Parti socialiste (France)|PS]]",
        'Parti Socialiste (Dissident)': " = [[Dissidence|diss]] [[Parti socialiste (France)|PS]]",
        'Pour La Semaine De 4 Jours': " = [[Semaine de quatre jours|Pour la semaine de 4 jours]]",
        'Mouvement Des Citoyens': " = [[Mouvement des citoyens (France)|MDC]]",
        'Energie Radicale': " = [[Mouvement des citoyens (France)|MDC]]",
        'Mouvement Républicain Et Citoyen': " = [[Mouvement républicain et citoyen|MRC]]",
        'Parti Socialiste': " = [[Parti socialiste (France)|PS]]",
        'Regions Et Peuples Solidaires': " = [[Régions et peuples solidaires|RPS]]",
        "Rassemblement Pour Initiative Citoyenne": " = {{abréviation|RIC|Rassemblement pour l'initiative citoyenne}}",
        "Mouvement Republique Et Democratie": " = {{abréviation|MRD|Mouvement république et démocratie}}",
        'Republique Et Democratie': " = {{abréviation|RD|République et démocratie}}",
        'Mouvement Democratie Alsacienne': " = {{abréviation|MDA|Mouvement Démocratie Alsacienne}}",
        'Socialiste Dissident': " = {{abréviation|SD|Socialiste Dissident}}",
        'Citoyennete Pour Tous De Maine-Et-Loire': " = {{abréviation|CML|Citoyennete pour tous de Maine-et-Loire}}",
        'Candidat Des Forces De Gauche, Ecologistes Et Republicains De Progres': " = {{abréviation|CFGERP|Candidat des Forces de Gauche, Ecologistes et Républicains de Progrés}}",
        'Gauche Independante': " = {{abréviation|GI|Gauche indépendante}}",
        'Nouvelle Gauche': " = {{abréviation|NG|Nouvelle Gauche}}",
        'Centre Gauche': " = {{abréviation|CG|Centre Gauche}}",
        'Alternative Unitaire Antiliberale': " = {{abréviation|AUA|Alternative Unitaire Antilibérale}}",
        'Gauche Nouvelle, Audacieuse, Realiste': " = {{abréviation|GNAR|Gauche Nouvelle, Audacieuse, Réaliste}}",
        'Carrefour Des Gauches': " = {{abréviation|CG|Carrefour des gauches}}",
        'Gauche Ouvriere Et Chretienne': " = {{abréviation|GOC|Gauche ouvrière et chrétienne}}",
        'Convention Pour Une Alternative Progressive': " = {{abréviation|CAP|Convention pour une alternative progressive}}",
        'Citoyens En Mouvement': " = {{abréviation|CM|Citoyens en Mouvement}}",
        'Mouvement Democratie Lorraine': " = {{abréviation|MDL|Mouvement Démocratie Lorraine}}",
        'Renouveau A Gauche': " = {{abréviation|RG|Renouveau à Gauche}}",
        'Initiative Republicaine': " = {{abréviation|IR|Initiative républicaine}}"
    }
    return print(switcher.get(argument, " = " + argument))

def switch_divers(argument):
    switcher = {
        'empty': " = Divers",
        'Le Trefle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|NE]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Representante Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecoloâ­Gistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecoâ­Logistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux, Union Nationale Ecologiste': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        "Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux, Presentes Par L'Union Nationale Ecologiste, Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        "Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux Presentes Par L'Union Nationale Ecologiste, Le Parti Pour La Defense Des Animaux Et Le Mouvement Universaliste": " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
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
        'Union Des Independants': " = {{abréviation|UI|Union des indépendants}}",
        'Moment D’Agir': " = {{abréviation|MA|Moment d'agir}}",
        'Front Liberation Des Oisifs Proletariens': " = {{abréviation|FLOP|Front libération des oisifs prolétariens}}",
        'Union Elargie Des Seniors': " = {{abréviation|UES|Union élargie des séniors}}",
        'Parti Des Musulmans De France': " = {{abréviation|PMF|Parti des musulmans de France}}",
        'Democrate Europeen': " = {{abréviation|DE|Démocrate Européen}}",
        'C.E.S.P.R.I.M.E.R  Autrement': " = {{abréviation|CESPRIMERA|C.E.S.P.R.I.M.E.R  Autrement}}",
        'Candidat De Marne Ecologie': " = {{abréviation|ME|Marne Ecologie}}",
        'Nationalforum Elsab-Lothringen Unabhã„Gig': " = {{abréviation|NEU|Nationalforum Elsab-Lothringen Unabhã„Gig}}",
        "Politique D'Action Citoyenne,Solidarite,": " = {{abréviation|PACS|Politique d'action citoyenne, solidarité}}",
        'Ecologie Nouvelle': " = {{abréviation|EN|Ecologie Nouvelle}}",
        'Des Animaux Et Mouvement Universaliste': " = {{abréviation|AMU|Des animaux et mouvement universaliste}}",
        'Ras Le Bol': " = {{abréviation|RB|Ras le bol}}",
        'Parti Du Ras Le Bol': " = {{abréviation|RB|Ras le bol}}",
        'Mouvement Ras Le Bol': " = {{abréviation|RB|Ras le bol}}",
        "Candidat De L'Union Nationale Ecologiste": " = {{abréviation|UNE|Union Nationale Ecologiste}}",
        "Stop A L'Autoroute": " = {{abréviation|SA|Stop à l'autoroute}}",
        "Defense Des Animaux Et Collectif National Defense Animale": " = {{abréviation|DACNDA|Défense des animaux et collectif national défense animale}}",
        "Candidate Du Parti Pour La Defense Des Animaux": " = {{abréviation|PDA|Parti pour la défense des animaux}}",
        "Solidarité Liberté Justice Paix": " = {{abréviation|SLJP|Solidarité Liberté Justice Paix}}",
        'Parti Pour La Defense Des Animaux Et Mouvement Universaliste': " = {{abréviation|AMU|Des animaux et mouvement universaliste}}",
        'Parti Pour La Defense Des Animaux': " = {{abréviation|PDA|Parti pour la défense des animaux}}",
        'Developpement Social Democratie De Proximite': " = {{abréviation|DSDP|Développement Social Démocratie de Proximité}}",
        'Parti Des Socioprofessionnels': " = {{abréviation|PS|Parti des socioprofessionnels}}",
        'Mouvement Pour Une Citoyennete Republicaine': " = {{abréviation|MCR|Mouvement pour une Citoyenneté Républicaine}}",
        "Parti D'En Rire": " = {{abréviation|PR|Parti d'en Rire}}",
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
        "Parti Blanc": " = {{abréviation|PB|Parti blanc}}",
        "Ordre Republicain Francais": " = {{abréviation|ORF|Ordre républicain français}}",
        "Reformes, Democratie Sante": " = {{abréviation|ORF|Réformes, démocratie santé}}",
        "Entreprise Emplois": " = {{abréviation|EE|Entreprise emplois}}",
        "Alliance Pour L'Ecologie Et La Democratie": " = {{abréviation|AED|Alliance pour l'écologie et la démocratie}}",
        "Droit De Chasse": " = {{abréviation|DC|Droit de chasse}}",
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
    return print(switcher.get(argument, " = " + argument))

def switch_extremedroite(argument):
    switcher = {
        'empty': " = [[Extrême droite en France|EXD]]",
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
        'Alliance Populaire': " = {{abréviation|AP|Alliance Populaire}}",
        'Mouvement De Rassemblement National': " = {{abréviation|MRN|Mouvement de Rassemblement National}}",
        "Alsace Debout Contre L'Insecurite Et L'Immigration": " = {{abréviation|ADII|Alsace debout contre l'insécurité et l'immigration}}",
        'Parti National Radical': " = {{abréviation|PNR|Parti National Radical}}",
        'Front Francais': " = {{abréviation|FF|Front Français}}",
        'Alternative Nationale': " = {{abréviation|AN|Alternative Nationale}}",
        'Savoie Independante': " = {{abréviation|SI|Savoie Indépendante}}",
        'Nouvelle Solidarite': " = {{abréviation|NS|Nouvelle Solidarité}}",
        'Parti National Republicain': " = {{abréviation|PNR|Parti national républicain}}",
        'Parti Ouvrier Europeen': " = [[Parti ouvrier européen|POE]]",
        'Solidarite Et Progres': " = {{abréviation|SP|Solidarité et Progrès}}",
        'Union Des Independants': " = {{abréviation|UI|Union des indépendants}}",
        'Alliance Populaire, Mouvement De Rassemblement National': " = {{abréviation|AP|Alliance populaire}} - {{abréviation|MRN|Mouvement de rassemblement national}}",
        "Candidate De L'Alliance Populaire": " = {{abréviation|AP|Alliance populaire}}",
        "Candidat De L'Alliance Populaire": " = {{abréviation|AP|Alliance populaire}}"
    }
    return print(switcher.get(argument, " = " + argument))

def switch_ecologiste(argument):
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
        'Mouvement Écologiste Indépendant': " = [[Mouvement écologiste indépendant|MEI]]",
        'Mouvement Ecologiste Independant': " = [[Mouvement écologiste indépendant|MEI]]",
        'Mouvement Hommes Animaux Nature': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Homme Nature Animaux': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Hommes-Animaux-Nature : Mhan': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Des Ecologistes Independants': " = [[Mouvement écologiste indépendant|MEI]]",
        'Cap 21': " = [[Cap21]]",
        'Citoyennete Action Participation Pour Le 21E Siecle': " = {{abréviation|CAP21e|Citoyenneté action participation pour le 21e siècle}}",
        'Une France Humaine': " = {{abréviation|FH|Une France Humaine}}",
        'Ecologie Pour L Alsace Du Nord': " = {{abréviation|FH|Écologie pour l'Alsace du nord}}",
        'Ecologie Artisanale': " = {{abréviation|EA|Écologie Artisanale}}",
        'Verts Alternatifs': " = {{abréviation|VA|Verts Alternatifs}}",
        'Verte Alternative': " = {{abréviation|VA|Verts Alternatifs}}",
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
        'Nouveaux Ecologistes': " = {{abréviation|NE|Nouveaux écologistes}}",
        'Confederation Des Ecologistes Independants': " = {{abréviation|CEI|Confédération des écologistes indépendants}}",
        'Souverainete Ecologie Ruralite': " = {{abréviation|SER|Souveraineté écologie ruralité}}",
        'Parti Pour La Defense Des Animaux': " = {{abréviation|DA|Parti pour la défense des animaux}}",
        'Ensemble, Ecologistes Et Solidaires': " = {{abréviation|EES|Ensemble, Écologistes et Solidaires}}",
        "Candidat Libre Pour Le Respect De L'Electeur": " = {{abréviation|CLRE|Candidat libre pour le respect de l'électeur}}",
        'Solidarite Ecologie Gauche Alternative': " = [[Les Alternatifs|SEGA]]",
        'Parti De L Entente': " = {{abréviation|PE|Parti de l'entente}}"
    }
    return print(switcher.get(argument, " = " + argument))

def switch_communiste(argument):
    switcher = {
        'empty': " = [[Communisme|COM]]",
        'Communistes': " = [[Communisme|COM]]",
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
        'Candidat De Rassemblement Pour Se Defendre Et Faire Du Neuf Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Rassemblement Pour Se Defendre Et Faire Du Neuf Presentee Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Rassemblement Pour Se Defendre Et Faire Du Neuf Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Rassemblement Des Forces De Gauche Presente Par Le Pcf': " = [[Parti communiste français|PCF]]",
        'Parti Communiste Francais Pour Le Rassemblement Des Forces Progressistes Et Le Changement': " = [[Parti communiste français|PCF]]",
        'Parti Communiste Francais, Pour Le Rassemblement Des Forces Progressistes Et Le Changement': " = [[Parti communiste français|PCF]]",
        'Parti Communiste': " = [[Parti communiste français|PCF]]",
        'Rassemblement Gauche Unie Et Anti Liberale': " = [[Gauche antilibérale|RGUAL]]",
        'Gauche Antiliberale': " = [[Gauche antilibérale|GA]]",
        'Candidat Rassemblement Pcf': " = [[Parti communiste français|PCF]]",
        'Gauche Alternative Et Antiliberale': " = [[Gauche antilibérale|GA]]",
        'Rassemblement Des Forces De Gauche': " = {{abréviation|RFG|Rassemblement des forces de gauche}}",
        'Mouvement Refondations': " = {{abréviation|MR|Mouvement Refondations}}",
        'Gauche Populaire Et Antiliberale Soutenue Par Pcf': " = {{abréviation|GPA|Gauche populaire et antilibérale - PCF}}"
    }
    return print(switcher.get(argument, " = " + argument))

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
#r = requests.get(url, params = {'format': 'json', 'query': query})
#data = r.json()

candidat_list = {}

#for i in range(0,len(data['results']['bindings'])):
#  candidat_list[remove_accents(data['results']['bindings'][i]['itemLabel']['value'])] = data['results']['bindings'][i]['sitelink']['value']

sys.argv = ['circo.py', '-d', "HAUTE-SAVOIE", '-y', '2012']
#on recupere les options utilisateurs
parser = argparse.ArgumentParser(description="Gap filling programms")
#recupere le fichier comportant les reads
parser.add_argument("-d", "--departement", required=True)
#recupere l annee
parser.add_argument("-y", "--year", required=True, type=int)
param = parser.parse_args()


def election(annee, departement):
    if annee == 2012:
        post_date_premier_tour = "11"
        post_moi = "juin"
        post_date_second_tour = "18"
        post_year = "2017"

        date_premier_tour = "10"
        moi = "juin"
        date_second_tour = "17"

        pre_date_premier_tour = "10"
        pre_moi = "juin"
        pre_date_second_tour = "12"
        pre_year = "2007"

        decennie = "2010"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi2007t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi2007t2_circ.xls', index_col=None)
    elif annee == 2007:
        post_date_premier_tour = "10"
        post_moi = "juin"
        post_date_second_tour = "17"
        post_year = "2012"

        date_premier_tour = "10"
        moi = "juin"
        date_second_tour = "12"

        pre_date_premier_tour = "9"
        pre_moi = "juin"
        pre_date_second_tour = "12"
        pre_year = "2002"

        decennie = "2000"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi2002t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi2002t2_circ.xls', index_col=None)
    elif annee == 2002:
        post_date_premier_tour = "10"
        post_moi = "juin"
        post_date_second_tour = "12"
        post_year = "2007"

        date_premier_tour = "9"
        moi = "juin"
        date_second_tour = "12"

        pre_date_premier_tour = "12"
        pre_moi = "mars"
        pre_date_second_tour = "21"
        pre_year = "1997"

        decennie = "2000"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1997t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1997t2_circ.xls', index_col=None)
    elif annee == 1997:
        post_date_premier_tour = "9"
        post_moi = "juin"
        post_date_second_tour = "12"
        post_year = "2002"

        date_premier_tour = "12"
        moi = "mars"
        date_second_tour = "21"

        pre_date_premier_tour = "12"
        pre_moi = "mars"
        pre_date_second_tour = "21"
        pre_year = "1993"

        decennie = "1990"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1993t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1993t2_circ.xls', index_col=None)
    elif annee == 1993:
        post_date_premier_tour = "12"
        post_moi = "mars"
        post_date_second_tour = "21"
        post_year = "1997"

        date_premier_tour = "12"
        moi = "mars"
        date_second_tour = "21"

        pre_date_premier_tour = "5"
        pre_moi = "juin"
        pre_date_second_tour = "12"
        pre_year = "1988"

        decennie = "1990"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1988t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1988t2_circ.xls', index_col=None)
    elif annee == 1988:
        post_date_premier_tour = "12"
        post_moi = "mars"
        post_date_second_tour = "21"
        post_year = "1993"

        date_premier_tour = "5"
        moi = "juin"
        date_second_tour = "12"

        pre_date_premier_tour = "14"
        pre_moi = "juin"
        pre_date_second_tour = "21"
        pre_year = "1981"

        decennie = "1980"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1981t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1981t2_circ.xls', index_col=None)
    elif annee == 1981:
        post_date_premier_tour = "5"
        post_moi = "juin"
        post_date_second_tour = "12"
        post_year = "1988"

        date_premier_tour = "14"
        moi = "juin"
        date_second_tour = "21"

        pre_date_premier_tour = "12"
        pre_moi = "mars"
        pre_date_second_tour = "18"
        pre_year = "1978"

        decennie = "1980"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1978t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1978t2_circ.xls', index_col=None)
    elif annee == 1978:
        post_date_premier_tour = "14"
        post_moi = "juin"
        post_date_second_tour = "21"
        post_year = "1981"

        date_premier_tour = "12"
        moi = "mars"
        date_second_tour = "18"

        pre_date_premier_tour = "4"
        pre_moi = "mars"
        pre_date_second_tour = "11"
        pre_year = "1973"

        decennie = "1970"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1973t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1973t2_circ.xls', index_col=None)
    elif annee == 1973:
        post_date_premier_tour = "12"
        post_moi = "mars"
        post_date_second_tour = "18"
        post_year = "1978"

        date_premier_tour = "4"
        moi = "mars"
        date_second_tour = "11"

        pre_date_premier_tour = "23"
        pre_moi = "juin"
        pre_date_second_tour = "30"
        pre_year = "1968"

        decennie = "1970"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1968t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1968t2_circ.xls', index_col=None)
    elif annee == 1968:
        post_date_premier_tour = "4"
        post_moi = "mars"
        post_date_second_tour = "11"
        post_year = "1973"

        date_premier_tour = "23"
        moi = "juin"
        date_second_tour = "30"

        pre_date_premier_tour = "5"
        pre_moi = "mars"
        pre_date_second_tour = "12"
        pre_year = "1967"

        decennie = "1960"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1967t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1967t2_circ.xls', index_col=None)
    elif annee == 1967:
        post_date_premier_tour = "23"
        post_moi = "juin"
        post_date_second_tour = "30"
        post_year = "1968"

        date_premier_tour = "5"
        moi = "mars"
        date_second_tour = "12"

        pre_date_premier_tour = "18"
        pre_moi = "novembre"
        pre_date_second_tour = "25"
        pre_year = "1962"

        decennie = "1960"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1962t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1962t2_circ.xls', index_col=None)
    elif annee == 1962:
        post_date_premier_tour = "5"
        post_moi = "mars"
        post_date_second_tour = "12"
        post_year = "1967"

        date_premier_tour = "18"
        moi = "novembre"
        date_second_tour = "25"

        pre_date_premier_tour = "23"
        pre_moi = "novembre"
        pre_date_second_tour = "30"
        pre_year = "1958"

        decennie = "1960"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)
        precedent_first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1958t1_circ.xls', index_col=None)
        precedent_second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi1958t2_circ.xls', index_col=None)
    elif annee == 1958:
        post_date_premier_tour = "18"
        post_moi = "novembre"
        post_date_second_tour = "25"

        date_premier_tour = "23"
        moi = "novembre"
        date_second_tour = "30"
        decennie = "1950"
        first_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't1_circ.xlsx', index_col=None)
        second_tour = pd.read_excel('/home/adrien/Documents/legis/excel_file/cdsp_legi' + str(annee) + 't2_circ.xlsx', index_col=None)

    ##first_tour_circo = find_circo(first_tour, departement, cironscription)
    ##second_tour_circo = find_circo(second_tour, departement, cironscription)

    dataframe_departement_first = find_departement(first_tour, departement)
    dataframe_departement_second = find_departement(second_tour, departement)
    precedent_dataframe_departement_first = find_departement(first_tour, departement)
    precedent_dataframe_departement_second = find_departement(second_tour, departement)

    nb_circonscription = dataframe_departement_first.shape[0]
    format_departement = departement.title()

    inscrit_first = int(dataframe_departement_first['Inscrits'].sum())
    votants_first = int(dataframe_departement_first['Votants'].sum())
    exprimes_first = int(dataframe_departement_first['Exprimés'].sum())
    nuls_first = int(dataframe_departement_first['Blancs et nuls'].sum())

    inscrit_second = int(dataframe_departement_second['Inscrits'].sum())
    votants_second = int(dataframe_departement_second['Votants'].sum())
    exprimes_second = int(dataframe_departement_second['Exprimés'].sum())
    nuls_second = int(dataframe_departement_second['Blancs et nuls'].sum())

    precedent_inscrit_first = int(precedent_dataframe_departement_first['Inscrits'].sum())
    precedent_votants_first = int(precedent_dataframe_departement_first['Votants'].sum())
    precedent_exprimes_first = int(precedent_dataframe_departement_first['Exprimés'].sum())
    precedent_nuls_first = int(precedent_dataframe_departement_first['Blancs et nuls'].sum())

    precedent_inscrit_second = int(precedent_dataframe_departement_second['Inscrits'].sum())
    precedent_votants_second = int(precedent_dataframe_departement_second['Votants'].sum())
    precedent_exprimes_second = int(precedent_dataframe_departement_second['Exprimés'].sum())
    precedent_nuls_second = int(precedent_dataframe_departement_second['Blancs et nuls'].sum())

    print("{{Infobox Élection")
    print(" | pays                   = France")
    print(" | date élection          = {{date|", date_premier_tour, "|", moi, "-|", annee, "-}} et {{date|", date_second_tour, "|", moi, "|", annee, "}}", sep = '')
    print(" | endispute              = ", nb_circonscription, " sièges de députés à l'[[Assemblée nationale (France)|Assemblée nationale]]", sep = '')
    print(" | élection précédente    = Élections législatives de ", pre_year, " en ", format_departement, sep = '')
    print(" | date précédente        = {{date|", pre_date_premier_tour, "|", pre_moi, "-|", pre_year, "-}} et {{date|", pre_date_second_tour, "|", pre_moi, "|", pre_year, "}}", sep = '')
    print(" | élection suivante      = Élections législatives de ", post_year, " en ", format_departement, sep = '')
    print(" | date suivante          = {{date|", post_date_premier_tour, "|", post_moi, "-|", post_year, "-}} et {{date|", post_date_second_tour, "|", post_moi, "|", post_year, "}}", sep = '')
    print(" | type                   = [[Élections législatives en France|Élections législatives]]")
    print(" | habitants              = ")
    print(" | enregistrés            = ", inscrit_first, sep = '')
    print(" | votants                = ", votants_first, sep = '')
    print(" | votants2               = ", votants_second, sep = '')
    print(" | participation          = ", round(votants_first/inscrit_first*100, 2), sep = '')
    print(" | participation ref      = ")
    print(" | participation pré      = ", round(precedent_votants_first/precedent_inscrit_first*100, 2), sep = '')
    print(" | participation2         = ", round(votants_second/inscrit_second*100, 2), sep = '')
    print(" | participation2 ref     = ")
    print(" | valables               = ", exprimes_first, sep = '')
    print(" | valables2              = ", exprimes_second, sep = '')
    print(" | nom élus               = députés")
    print(" | campagne               = ")
    print(" | débat                  = ")
    print("}}")

    corps_post(dataframe_departement_first)

    print("== Élus ==")
    print("\n")
    print("{| style=\"text-align: center;line-height:14px;\" class=\"wikitable centre\"")
    print("|+")
    print("! scope=\"col\" |Circonscription")
    print("! scope=\"col\" |Député sortant")
    print("! colspan=\"2\" scope=\"col\" |Parti")
    print("! scope=\"col\" |Député élu ou réélu")
    print("! colspan=\"2\" scope=\"col\" |Parti")
    print("|-")




    print("== Notes et références ==")
    print("{{Références}}")
    print("\n")
    print("== Articles connexes ==")
    print("* [[Liste des circonscriptions législatives de la ", format_departement, "]]", sep = '')
    print("* [[Liste des députés de la ", format_departement, "]]", sep = '')
    print("* [[Élections législatives françaises de ", annee, "]]", sep = '')
    print("\n")
    print("{{Palette|Élections législatives de ", annee, " en France}}", sep = '')
    print("{{Portail|années ", decennie, "|politique française|", format_departement, "}}", sep = '')
    print("\n")
    print("[[Catégorie:Élections législatives françaises de ", annee, "|Législatives, ", annee, "]]", sep = '')
    print("[[Catégorie:Élection en ", format_departement, "|", format_departement, "]]", sep = '')

def find_departement(dataframe, departement):
    is_dep =  dataframe['département'] == departement
    dataframe_departement = dataframe[is_dep]
    return dataframe_departement

election(param.year, param.departement)