import argparse
import pandas as pd
import sys
import gc

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
            if v != [0, 0]:
                print("| candidat", i," = Inconnu", sep = '')
                partie_name(k, i)
                print("| suffrages", i, " = ", v[0], sep = '')
                couleur_hex(k, i)
                i += 1
        print("}}")

def corps_post(premier_tour, second_tour, tour):
    dicocirc_premier = premier_tour.to_dict(orient='list')
    dicocirc_second = second_tour.to_dict(orient='list')
    diconom = {}
    dicovoix = {}
    dicolabel = {}
    u = 1
    check = 'BEGIN'
    nuance = str(u) + ' nuance'
    while type(check) != float:
        prenom = str(u) + ' Prénom candidat'
        nom = str(u) + ' Nom candidat'
        voix = str(u) + ' voix'
        label = str(u) + ' Etiquette liste'
        another_lab = dicocirc_premier[nuance][0] + dicocirc_premier[nom][0]
        diconom[another_lab] = [dicocirc_premier[prenom][0].title(), dicocirc_premier[nom][0].title()]
        dicovoix[another_lab] = [int(dicocirc_premier[voix][0])]
        if type(dicocirc_premier[label][0]) == float:
            dicolabel[another_lab] = 'empty'
        else:
            dicolabel[another_lab] = dicocirc_premier[label][0].title()
        u += 1
        nuance = str(u) + ' nuance'
        check = dicocirc_premier[nuance][0]

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
            print("| candidat", i, " = ", diconom[k][0], " ", diconom[k][1], sep = '')
            partie_name_post(k, i, dicolabel)
            print("| suffrages", i, " = ", dicovoix[k][0], sep = '')
            if len(dicovoix[k]) == 2:
                print("| suffrages", i, "b = ", dicovoix[k][1], sep = '')
            else:
                pass
            couleur_hex_post(k, i, dicolabel)
            i += 1
        print("}}")
    else:
        i = 1
        for k, v in sorted(dicovoix.items(), key=lambda x: x[1], reverse=True):
            print("| candidat", i, " = ", diconom[k][0], " ", diconom[k][1], sep = '')
            partie_name_post(k, i, dicolabel)
            print("| suffrages", i, " = ", dicovoix[k][0], sep = '')
            couleur_hex_post(k, i, dicolabel)
            i += 1
        print("}}")

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
        "Reseau Nouvelle Donne": " = {{Infobox Parti politique français/couleurs|-fuchsia}}",
        "Union Democratique Bretonne": " = {{Infobox Parti politique français/couleurs|-UDB}}",
    }
    return print_hex(switcher.get(argument, " = {{Infobox Parti politique français/couleurs|-DIV}}"), order_number)

def switch_extremedroite_hex(argument, order_number):
    switcher = {
        'Mouvement National Republicain': " = {{Infobox Parti politique français/couleurs|-MNR}}",
        "Mnr - Contre L'Immigration-Islamisation, L'Insecurite": " = {{Infobox Parti politique français/couleurs|-MNR}}",
        'Mouvement National Republicain': " = [[Mouvement national républicain|MNR]]",
        'Union De La Droite Nationale': " = [[Union de la droite nationale|UDN]]",
        'Parti Anti-Sioniste': " = [[Parti antisioniste|PAS]]",
        'Defendons La Chasse Et Nos Traditions': " = {{abréviation|DCT|Défendons la chasse et nos traditions}}",
        'Rassemblement Republicain Pour L Union Centriste': " = {{abréviation|RRUC|Rassemblement républicain pour l'union centriste}}",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Alliance Populaire': " = {{abréviation|AP|Alliance Populaire}}",
        'Parti National Republicain': " = {{abréviation|PNR|Parti national républicain}}",
        'Parti Ouvrier Europeen': " = [[Parti ouvrier européen|POE]]",
        'Alliance Populaire, Mouvement De Rassemblement National': " = {{abréviation|AP|Alliance populaire}} - {{abréviation|MRN|Mouvement de rassemblement national}}"
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
        'FDG': print_partie(" = [[Front de gauche (France)|FDG]]", order_number),
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

def switch_regionalisme(argument, order_number):
    switcher = {
        'empty': " = [[Régionalisme (politique)|REG]]"
    }
    return switcher.get(print_partie(argument, order_number), " = " + argument)

def switch_extremegauche(argument, order_number):
    switcher = {
        'empty': " = [[Extrême gauche en France|EXG]]",
        'Lutte Ouvrière': " = [[Lutte ouvrière|LO]]",
        'Lutte Ouvriere': " = [[Lutte ouvrière|LO]]",
        'Ligue Communiste Revolutionnaire': " = [[Ligue communiste révolutionnaire|LCR]]",
        'Nouveau Parti Anticapitaliste': " = [[Nouveau Parti anticapitaliste|NPA]]",
        'Alternatifs (Solidarite, Ecologie, Gauche Alternative)': " = [[Les Alternatifs]]",
        'Les Alternatifs': " = [[Les Alternatifs]]",
        'Extreme Gauche': " = [[Extrême gauche en France|EXG]]",
        'Extrême gauche': " = [[Extrême gauche en France|EXG]]",
        'Parti Des Travailleurs': " = [[Parti des travailleurs (France)|PT]]",
        'Gauche Alternative 2007': " = [[Gauche alternative 2007|GP2007]]",
        'Alternative Rouge Et Verte': " = [[Alternative rouge et verte|ARV]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Solidarite, Ecologie, Gauche Alternative (Sega)': " = [[Gauche alternative 2007|SEGA]]",
        'Solidarite Ecologie Gauche Alternative': " = [[Gauche alternative 2007|SEGA]]",
        'Candidat D Initiative Pour Une Nouvelle Politique A Gauche': " = {{abréviation|CINPG|Candidat d'initiative pour une nouvelle politique à gauche}}",
        'Voix Des Travailleurs': " = [[Voix des travailleurs|VdT]]",
        "Union Pour L'Ecologie Et La Democratie": " = {{abréviation|UED|Union pour l'écologie et la démocratie}}",
        "Pole Rennaissance Communiste En France": " = [[Pôle de renaissance communiste en France|PRCF]]",
        'Union Pour La Gauche Renovee': " = {{abréviation|UGR|Union pour la gauche rénovée}}",
        'Tous Ensemble A Gauche': " = {{abréviation|TEG|Tous ensemble à gauche}}",
        "Parti Ouvrier Indépendant": " = [[Parti ouvrier indépendant|POI]]",
        'A Gauche Vraiment': " = {{abréviation|GV|A gauche vraiment}}",
        'Rassemblement Utile A Tous': " = {{abréviation|RUT|Rassemblement utile à tous}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_diversdroite(argument, order_number):
    switcher = {
        'empty': " = [[Divers droite|DVD]]",
        'Mouvement Pour La France': " = [[Mouvement pour la France|MPF]]",
        'Debout La République': " = [[Debout la France|DLR]]",
        'Debout La Republique': " = [[Debout la France|DLR]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Centre National Des Independants Et Paysans': " = [[Centre national des indépendants et paysans|CNIP]]",
        'Centre National Des Independants': " = [[Centre national des indépendants et paysans|CNI]]",
        'Parti Chrétien-Démocrate': " = [[VIA, la voie du peuple|PCD]]",
        'Union Républicaine Populaire': " = [[Union populaire républicaine (2007)|UPR]]",
        'Divers Droite': " = [[Divers droite|DVD]]",
        'La Droite Independante (Mpf)': " = [[La droite indépendante|LDI]]",
        'Rassemblement Pour La France': " = [[Rassemblement pour la France|RPF]]",
        'Union Des Démocrates Pour La République': " = [[Union des démocrates pour la République|UDR]]",
        'Rassemblement Pour La Republique': " = [[Rassemblement pour la République|RPR]]",
        'Droite Liberale Chretienne': " = [[Droite libérale-chrétienne|DLC]]",
        'Alternative Liberale': " = [[Alternative libérale|AL]]",
        'Parti De La Loi Naturelle': " = [[Parti de la loi naturelle|PLN]]",
        'Le Trefle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Union De La Droite Republicaine': " = Union de la droite republicaine",
        'Mouvement Des Reformateurs': " = [[Mouvement des réformateurs|MDR]]",
        'Parti Pour La Liberte': " = {{abréviation|PL|Parti pour la liberté}}",
        'Pour La Justice Et La Prosperite De La France': " = {{abréviation|JPF|Pour la justice et la prospérité de la France}}",
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
        'Socialiste Dissidente': " = [[Dissidence|diss]] [[Parti socialiste (France)|PS]]",
        'Pour La Semaine De 4 Jours': " = [[Semaine de quatre jours|Pour la semaine de 4 jours]]",
        'Mouvement Des Citoyens': " = [[Mouvement des citoyens (France)|MDC]]",
        'Energie Radicale': " = [[Mouvement des citoyens (France)|MDC]]",
        'Mouvement Républicain Et Citoyen': " = [[Mouvement républicain et citoyen|MRC]]",
        'Parti Socialiste': " = [[Parti socialiste (France)|PS]]",
        'Republique Et Democratie': " = {{abréviation|RD|République et démocratie}}",
        'Gauche Independante': " = {{abréviation|GI|Gauche indépendante}}",
        'Initiative Republicaine': " = {{abréviation|IR|Initiative républicaine}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_divers(argument, order_number):
    switcher = {
        'empty': " = Divers",
        'Le Trefle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux': " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]",
        'Parti De La Loi Naturelle': " = [[Parti de la loi naturelle|PLN]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Chasse Peche Nature Traditions': " = [[Le Mouvement de la ruralité|CPNT]]",
        'Chasse Peche Nature Et Traditions': " = [[Le Mouvement de la ruralité|CPNT]]",
        'Parti Federaliste': " = [[Parti fédéraliste (France)|PF]]",
        'Regions Et Peuples Solidaires': " = [[Solidarité et progrès|SP]]",
        'Solidarité Et Progrès': " = [[Solidarité et progrès|SP]]",
        'Parti Humaniste': " = [[Parti humaniste (France)|PH]]",
        'Rassemblement Des Contribuables Francais': " = [[Nicolas Miguet|Rassemblement des contribuables francais]]",
        'Parti Rachid Nekkaz': " = [[Rachid Nekkaz|Parti Rachid Nekkaz]]",
        'Parti Occitan':  " = [[Partit occitan|PO]]",
        'Energies Democrates': " = [[Christian Blanc|Energies democrates]]",
        'Parti Des Socioprofessionnels': " = {{abréviation|PS|Parti des socioprofessionnels}}",
        "Rassemblement Pour L'Initiative Citoyenne": " = {{abréviation|RIC|Rassemblement pour l'initiative citoyenne}}",
        "Gip - Democratie Active": " = {{abréviation|GIP|GIP - Démocratie active}}",
        "La France En Action": " = {{abréviation|FA|La France en action}}",
        'Union Nationale Ecologiste Sans Emploi': " = {{abréviation|UNESE|Union nationale écologiste sans emploi}}",
        "Parti Des Droits De L'Homme": " = {{abréviation|PDH|Parti des droits de l'Homme}}",
        "Solidaires Regions Ecologie": " = {{abréviation|SRE|Solidaires régions écologie}}",
        "Union Des Citoyens Independants": " = {{abréviation|UCI|Union des citoyens independants}}",
        "Divers": " = {{abréviation|DIV|Divers}}",
        "Union Pour L'Ecologie Et La Democratie": " = {{abréviation|UED|Union pour l'écologie et la démocratie}}",
        "Gard Fraternite": " = {{abréviation|GF|Gard Fraternité}}",
        "Parti Du Vote Blanc": " = {{abréviation|PVB|Parti du vote blanc}}",
        "Parti Pirate": " = [[Parti pirate (France)|PR]]",
        "Parti De La Nation Occitane": " = [[Parti de la nation occitane|PNO]]",
        "Rassemblement Populaire Local": " = {{abréviation|RPL|Rassemblement populaire local}}",
        "Reseau Nouvelle Donne": " = [[Nouvelle Donne (parti politique)|ND]]",
        "Concordat Citoyen": " = {{abréviation|CC|Concordat citoyen}}",
        "Convergence Ecologie Solidarite": " = {{abréviation|CES|Convergence écologie solidarité}}",
        "Parti Blanc": " = {{abréviation|PB|Parti blanc}}",
        "Ordre Republicain Francais": " = {{abréviation|ORF|Ordre républicain français}}",
        "Reformes, Democratie Sante": " = {{abréviation|ORF|Réformes, démocratie santé}}",
        "Entreprise Emplois": " = {{abréviation|EE|Entreprise emplois}}",
        "Alliance Pour L'Ecologie Et La Democratie": " = {{abréviation|AED|Alliance pour l'écologie et la démocratie}}",
        "Droit De Chasse": " = {{abréviation|DC|Droit de chasse}}",
        "Union Democratique Bretonne": " = [[Union démocratique bretonne|UDB]]",
        "Parti De La Loi Naturelle (Pln)": " = [[Parti de la loi naturelle|PLN]]"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_extremedroite(argument, order_number):
    switcher = {
        'empty': " = [[Extrême droite en France|EXD]]",
        "Mnr - Contre L'Immigration-Islamisation, L'Insecurite": " = [[Mouvement national républicain|MNR]]",
        'Mouvement National Republicain': " = [[Mouvement national républicain|MNR]]",
        'Union De La Droite Nationale': " = [[Union de la droite nationale|UDN]]",
        'Parti Anti-Sioniste': " = [[Parti antisioniste|PAS]]",
        'Defendons La Chasse Et Nos Traditions': " = {{abréviation|DCT|Défendons la chasse et nos traditions}}",
        'Rassemblement Republicain Pour L Union Centriste': " = {{abréviation|RRUC|Rassemblement républicain pour l'union centriste}}",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Alliance Populaire': " = {{abréviation|AP|Alliance Populaire}}",
        'Parti National Republicain': " = {{abréviation|PNR|Parti national républicain}}",
        'Parti Ouvrier Europeen': " = [[Parti ouvrier européen|POE]]",
        'Alliance Populaire, Mouvement De Rassemblement National': " = {{abréviation|AP|Alliance populaire}} - {{abréviation|MRN|Mouvement de rassemblement national}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_ecologiste(argument, order_number):
    switcher = {
        'Ecologiste': " = [[Écologisme|ECO]]",
        'empty': " = [[Écologisme|ECO]]",
        'Génération Écologie': " = [[Génération écologie|GE]]",
        'Generation Ecologie': " = [[Génération écologie|GE]]",
        'Les Verts': " = [[Les Verts (France)|LV]]",
        'Sans Etiquette': " = [[Sans étiquette|SE]]",
        'Europe-Ecologie-Les Verts': " = [[Europe Écologie Les Verts|EELV]]",
        'Alliance Ecologiste Indépendante': " = [[Alliance écologiste indépendante|AEI]]",
        'Le Trefle': " = [[Le Trèfle - Les nouveaux écologistes|Le Trèfle]]",
        'Le Trèfle - Les Nouveaux Ecologistes': " = [[Le Trèfle - Les nouveaux écologistes|Le Trèfle]]",
        'Mouvement Écologiste Indépendant': " = [[Mouvement écologiste indépendant|MEI]]",
        'Mouvement Ecologiste Independant': " = [[Mouvement écologiste indépendant|MEI]]",
        'Mouvement Hommes Animaux Nature': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Homme Nature Animaux': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Mouvement Hommes-Animaux-Nature : Mhan': " = [[Mouvement hommes animaux nature|MHAN]]",
        'Citoyennete Action Participation Pour Le 21E Siecle': " = {{abréviation|CAP21e|Citoyenneté action participation pour le 21e siècle}}",
        'Union Nationale Ecologiste': " = {{abréviation|UNE|Union nationale écologiste}}",
        'Ecologie Et Citoyens': " = {{abréviation|EC|Ecologie et citoyens}}",
        'Ecologiste Independant': " = {{abréviation|EI|Ecologiste indépendant}}",
        'Parti Ecologiste': " = [[Parti écologiste|PE]]",
        'Renouveau Ecologique': " = {{abréviation|RE|Renouveau écologique}}",
        'Nouveaux Ecologistes': " = {{abréviation|NE|Nouveaux écologistes}}",
        'Confederation Des Ecologistes Independants': " = {{abréviation|CEI|Confédération des écologistes indépendants}}",
        'Souverainete Ecologie Ruralite': " = {{abréviation|SER|Souveraineté écologie ruralité}}",
        'Parti Pour La Defense Des Animaux': " = {{abréviation|DA|Parti pour la défense des animaux}}",
        'Parti De L Entente': " = {{abréviation|PE|Parti de l'entente}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

def switch_communiste(argument, order_number):
    switcher = {
        'empty': " = [[Communisme|COM]]",
        'Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Presente Par Le Parti Comâ­Muniste Francais': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Presente Par Le Pcf': " = [[Parti communiste français|PCF]]",
        'Candidat De Rassemblement Presente Par Le Parti Communiste Francais': " = [[Parti communiste français|PCF]]",
        'Candidat Rassemblement Pcf': " = [[Parti communiste français|PCF]]",
        'Rassemblement Des Forces De Gauche': " = {{abréviation|RFG|Rassemblement des forces de gauche}}",
        'Gauche Populaire Et Antiliberale Soutenue Par Pcf': " = {{abréviation|GPA|Gauche populaire et antilibérale - PCF}}"
    }
    return print_partie(switcher.get(argument, " = " + argument), order_number)

sys.argv = ['circo.py', '-d', "ISERE", '-c', '1']
#on recupere les options utilisateurs 
parser = argparse.ArgumentParser(description="Gap filling programms")
#recupere le fichier comportant les reads
parser.add_argument("-d", "--departement", required=True)
#recupere le fichier comportant le start et stop
parser.add_argument("-c", "--circo", required=True, type=int)
param = parser.parse_args()

# #
# 1958
# #

t1958a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1958t1_circ.xls', index_col=None)
t1958b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1958t2_circ.xls', index_col=None)

t1958b_circo = find_circo(t1958b, param.departement, param.circo)

if t1958b_circo.empty:
    pass
else:
    monotour = exist_second(t1958b_circo)
    print("| titre = Résultats des élections législatives des 23 et 30 novembre 1958 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 23/11/1958 par circonscription, cdsp_legi1958t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    t1958a_circo = find_circo(t1958a, param.departement, param.circo)
    premier_tour(t1958a_circo)
    subseta = t1958a_circo.iloc[:,7:t1958a_circo.size]
    subsetb = t1958b_circo.iloc[:,8:t1958b_circo.size]
    corps(subseta, subsetb, monotour, t1958b_circo)

    del (t1958a, t1958b, t1958b_circo, t1958a_circo)
    gc.collect()

# #
# 1962
# #

t1962a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1962t1_circ.xls', index_col=None)
t1962b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1962t2_circ.xls', index_col=None)

t1962b_circo = find_circo(t1962b, param.departement, param.circo)

if t1962b_circo.empty:
    pass
else:
    monotour = exist_second(t1962b_circo)
    print("| titre = Résultats des élections législatives des 18 et 25 novembre 1962 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 18/11/1962 par circonscription, cdsp_legi1962t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    t1962a_circo = find_circo(t1962a, param.departement, param.circo)
    premier_tour(t1962a_circo)
    subseta = t1962a_circo.iloc[:,7:t1962a_circo.size]
    subsetb = t1962b_circo.iloc[:,8:t1962b_circo.size]
    corps(subseta, subsetb, monotour, t1962b_circo)

    del (t1962a, t1962b, t1962b_circo, t1962a_circo)

    gc.collect()

# #
# 1967
# #

t1967a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1967t1_circ.xls', index_col=None)
t1967b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1967t2_circ.xls', index_col=None)

t1967b_circo = find_circo(t1967b, param.departement, param.circo)

if t1967b_circo.empty:
    pass
else:
    monotour = exist_second(t1967b_circo)
    print("| titre = Résultats des élections législatives des 5 et 12 mars 1967 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 05/03/1967 par circonscription, cdsp_legi1967t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    t1967a_circo = find_circo(t1967a, param.departement, param.circo)
    premier_tour(t1967a_circo)
    subseta = t1967a_circo.iloc[:,7:t1967a_circo.size]
    subsetb = t1967b_circo.iloc[:,8:t1967b_circo.size]
    corps(subseta, subsetb, monotour, t1967b_circo)

    del (t1967a, t1967b, t1967b_circo, t1967a_circo)

    gc.collect()

# #
# 1968
# #

t1968a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1968t1_circ.xls', index_col=None)
t1968b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1968t2_circ.xls', index_col=None)

t1968b_circo = find_circo(t1968b, param.departement, param.circo)

if t1968b_circo.empty:
    pass
else:
    monotour = exist_second(t1968b_circo)
    print("| titre = Résultats des élections législatives des 23 et 30 juin 1968 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 23/06/1968 par circonscription, cdsp_legi1968t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    t1968a_circo = find_circo(t1968a, param.departement, param.circo)
    premier_tour(t1968a_circo)
    subseta = t1968a_circo.iloc[:,7:t1968a_circo.size]
    subsetb = t1968b_circo.iloc[:,8:t1968b_circo.size]
    corps(subseta, subsetb, monotour, t1968b_circo)

    del (t1968a, t1968b, t1968b_circo, t1968a_circo)

    gc.collect()

# #
# 1973
# #

t1973a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1973t1_circ.xls', index_col=None)
t1973b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1973t2_circ.xls', index_col=None)

t1973b_circo = find_circo(t1973b, param.departement, param.circo)

if t1973b_circo.empty:
    pass
else:
    monotour = exist_second(t1973b_circo)
    print("| titre = Résultats des élections législatives des 4 et 11 mars 1973 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 11/03/1973 par circonscription, cdsp_legi1973t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    t1973a_circo = find_circo(t1973a, param.departement, param.circo)
    premier_tour(t1973a_circo)
    subseta = t1973a_circo.iloc[:,7:t1973a_circo.size]
    subsetb = t1973b_circo.iloc[:,8:t1973b_circo.size]
    corps(subseta, subsetb, monotour, t1973b_circo)

    del (t1973a, t1973b, t1973b_circo, t1973a_circo)

    gc.collect()

# #
# 1978
# #

t1978a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1978t1_circ.xls', index_col=None)
t1978b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1978t2_circ.xls', index_col=None)

t1978b_circo = find_circo(t1978b, param.departement, param.circo)

if t1978b_circo.empty:
    pass
else:
    monotour = exist_second(t1978b_circo)
    print("| titre = Résultats des élections législatives des 12 et 18 mars 1978 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 12/03/1978 par circonscription, cdsp_legi1978t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    t1978a_circo = find_circo(t1978a, param.departement, param.circo)
    premier_tour(t1978a_circo)
    subseta = t1978a_circo.iloc[:,7:t1978a_circo.size]
    subsetb = t1978b_circo.iloc[:,8:t1978b_circo.size]
    corps(subseta, subsetb, monotour, t1978b_circo)

    del (t1978a, t1978b, t1978b_circo, t1978a_circo)

    gc.collect()

# #
# 1981
# #

t1981a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1981t1_circ.xls', index_col=None)
t1981b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1981t2_circ.xls', index_col=None)

t1981b_circo = find_circo(t1981b, param.departement, param.circo)
t1981a_circo = find_circo(t1981a, param.departement, param.circo)

if t1981a_circo.empty:
    pass
else:
    monotour = exist_second_post(t1981b_circo)
    print("| titre = Résultats des élections législatives des 14 et 21 juin 1981 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 14/06/1981 par circonscription, cdsp_legi1981t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    premier_tour(t1981a_circo)
    subseta = t1981a_circo.iloc[:,6:t1981a_circo.size]
    subsetb = t1981b_circo.iloc[:,7:t1981b_circo.size]
    corps(subseta, subsetb, monotour, t1981b_circo)

    del (t1981a, t1981b, t1981b_circo, t1981a_circo)

    gc.collect()

##
# 1988
##

t1988a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1988t1_circ.xls', index_col=None)
t1988b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1988t2_circ.xls', index_col=None)

t1988b_circo = find_circo(t1988b , param.departement, param.circo)
t1988a_circo = find_circo(t1988a, param.departement, param.circo)

if t1988a_circo.empty:
    pass
else:
    monotour = exist_second_post(t1988b_circo)
    print("| titre = Résultats des élections législatives des 5 et 12 juin 1988 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 05/06/1988 par circonscription, cdsp_legi1988t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    premier_tour(t1988a_circo)
    corps_post(t1988a_circo, t1988b_circo, monotour)

    del (t1988a, t1988b, t1988b_circo, t1988a_circo)

    gc.collect()

##
# 1993
##

t1993a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1993t1_circ.xls', index_col=None)
t1993b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1993t2_circ.xls', index_col=None)

t1993b_circo = find_circo(t1993b , param.departement, param.circo)
t1993a_circo = find_circo(t1993a, param.departement, param.circo)

if t1993a_circo.empty:
    pass
else:
    monotour = exist_second_post(t1993b_circo)
    print("| titre = Résultats des élections législatives des 21 et 12 mars 1993 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 21/03/1993 par circonscription, cdsp_legi1993t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    premier_tour(t1993a_circo)
    corps_post(t1993a_circo, t1993b_circo, monotour)

    del (t1993a, t1993b, t1993b_circo, t1993a_circo)

    gc.collect()

##
# 1997
##

t1997a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1997t1_circ.xls', index_col=None)
t1997b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1997t2_circ.xls', index_col=None)

t1997b_circo = find_circo(t1997b , param.departement, param.circo)
t1997a_circo = find_circo(t1997a, param.departement, param.circo)

if t1997a_circo.empty:
    pass
else:
    monotour = exist_second_post(t1997b_circo)
    print("| titre = Résultats des élections législatives des 21 et 12 mars 1997 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 21/03/1997 par circonscription, cdsp_legi1997t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    premier_tour(t1997a_circo)
    corps_post(t1997a_circo, t1997b_circo, monotour)

    del (t1997a, t1997b, t1997b_circo, t1997a_circo)

    gc.collect()

##
# 2002
##

t2002a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2002t1_circ.xls', index_col=None)
t2002b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2002t2_circ.xls', index_col=None)

t2002b_circo = find_circo(t2002b , param.departement, param.circo)
t2002a_circo = find_circo(t2002a, param.departement, param.circo)

if t2002a_circo.empty:
    pass
else:
    monotour = exist_second_post(t2002b_circo)
    print("| titre = Résultats des élections législatives des 9 et 12 juin 2002 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 09/06/2002 par circonscription, cdsp_legi2002t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    premier_tour(t2002a_circo)
    corps_post(t2002a_circo, t2002b_circo, monotour)

    del (t2002a, t2002b, t2002b_circo, t2002a_circo)

    gc.collect()

##
# 2007
##

t2007a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2007t1_circ.xls', index_col=None)
t2007b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2007t2_circ.xls', index_col=None)

t2007b_circo = find_circo(t2007b , param.departement, param.circo)
t2007a_circo = find_circo(t2007a, param.departement, param.circo)

if t2007a_circo.empty:
    pass
else:
    monotour = exist_second_post(t2007b_circo)
    print("| titre = Résultats des élections législatives des 10 et 12 juin 2007 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 10/06/2007 par circonscription, cdsp_legi2007t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    premier_tour(t2007a_circo)
    corps_post(t2007a_circo, t2007b_circo, monotour)

    del (t2007a, t2007b, t2007b_circo, t2007a_circo)

    gc.collect()

##
# 2012
##

t2012a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2012t1_circ.xlsx', index_col=None)
t2012b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2012t2_circ.xlsx', index_col=None)

t2012b_circo = find_circo(t2012b , param.departement, param.circo)
t2012a_circo = find_circo(t2012a, param.departement, param.circo)

if t2012a_circo.empty:
    pass
else:
    monotour = exist_second_post(t2012b_circo)
    print("| titre = Résultats des élections législatives des 10 et 17 juin 2012 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
    print("| references = <ref>Résultats des élections législatives françaises premier tour du 10/06/2012 par circonscription, cdsp_legi2012t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

    premier_tour(t2012a_circo)
    corps_post(t2012a_circo, t2012b_circo, monotour)

    del (t2012a, t2012b, t2012b_circo, t2012a_circo)

    gc.collect()
