import argparse
import pandas as pd
import sys

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
                dicocirc[k].append(int(v))
        print("| inscrits2 = ", int(dataframe_second['Inscrits']), sep = '')
        print("| votants2 = ", int(dataframe_second['Votants']), sep = '')
        print("| exprimes2 = ", int(dataframe_second['Exprimés']), sep = '')
        i = 1
        for k, v in sorted(dicocirc.items(), key=lambda x: x[1], reverse=True):
            if v != [0, 0]:
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

def couleur_hex(col_name, order_number):
    if col_name == 'COM':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PCF}}", sep = '')
    elif col_name == 'COM2' or col_name == 'OCR' or col_name == 'OCI':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-COM}}", sep = '')
    elif col_name == 'UFD' or col_name == 'RADUFD':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UFD}}", sep = '')
    elif col_name == 'SFIO':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-SFIO}}", sep = '')
    elif col_name == 'RADSOC' or col_name == 'RADCENT' or col_name == 'DVG' or col_name == 'REFRAD' or col_name == 'RADICAUX GAUCHE':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DVG}}", sep = '')
    elif col_name == 'UDSRMIN':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UDSR}}", sep = '')
    elif col_name == 'UNR' or col_name == 'UNR-UDT':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UNR}}", sep = '')
    elif col_name == 'CRR' or col_name == 'DIVGAUL' or col_name == 'MOD' or col_name == 'POUJ' or col_name == 'RADDROIT' or col_name == 'ALLREP' or col_name == 'DIVMAJ' or col_name == 'DVD' or col_name == 'DIVURP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DVD}}", sep = '')
    elif col_name == 'MRP' or col_name == 'MRPVREP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-MRP}}", sep = '')
    elif col_name == 'CNI':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-CNIP}}", sep = '')
    elif col_name == 'EXD':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-EXD}}", sep = '')
    elif col_name == 'DIV' or col_name == 'TD' or col_name == 'MDR' or col_name == 'DIVREF' or col_name == 'GAULOPP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DIV}}", sep = '')
    elif col_name == 'PSU':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PSU}}", sep = '')
    elif col_name == 'EXG' or col_name == 'FRONT':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-EXG}}", sep = '')
    elif col_name == 'INDVREP' or col_name == 'RIURP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-RI}}", sep = '')
    elif col_name == 'FGDS':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-FGDS}}", sep = '')
    elif col_name == 'UDR' or col_name == 'RIUDR' or col_name == 'UDRURP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UDR}}", sep = '')
    elif col_name == 'RALLIE' or col_name == 'CDP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-CDP}}", sep = '')
    elif col_name == 'REG':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-REG}}", sep = '')
    elif col_name == 'LO':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-LO}}", sep = '')
    elif col_name == 'LCR':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-LCR}}", sep = '')
    elif col_name == 'SOC':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PS}}", sep = '')
    elif col_name == 'MRG':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PRG}}", sep = '')
    elif col_name == 'CDURP' or col_name == 'CDPURP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-CD}}", sep = '')
    elif col_name == 'PSMRG':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PS}}", sep = '')
    elif col_name == 'ECO':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-ECO}}", sep = '')
    elif col_name == 'UDF' or col_name == 'UDF-RPR':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UDF}}", sep = '')
    elif col_name == 'RPR':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-RPR}}", sep = '')
    elif col_name == 'FRN':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-FN}}", sep = '')
    elif col_name == 'CENTDEM':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-CD}}", sep = '')
    else:
        print('error', col_name)

def couleur_hex_post(col_name, order_number, dictionary):
    if col_name[:3] == 'FDG':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-FG}}", sep = '')
    elif col_name[:5] == 'MODEM':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-MODEM}}", sep = '')
    elif col_name[:3] == 'UMP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UMP}}", sep = '')
    elif col_name[:3] == 'SOC':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-SOC}}", sep = '')
    elif col_name[:5] == 'NouvC':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-NC}}", sep = '')
    elif col_name[:3] == 'PRG' or col_name == 'RDG':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PRG}}", sep = '')
    elif col_name[:4] == 'PSLE':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-LC}}", sep = '')
    elif col_name[:3] == 'RPR':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-RPR}}", sep = '')
    elif col_name[:3] == 'UDF':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UDF}}", sep = '')
    elif col_name[:3] == 'GEC':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-GE}}", sep = '')
    elif col_name[:3] == 'SDC':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PS}}", sep = '')
    elif col_name[:3] == 'VEC':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-Verts}}", sep = '')
    elif col_name[:3] == 'FRN':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-FN}}", sep = '')
    elif col_name[:3] == 'MAJ':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DIV}}", sep = '')
    elif col_name[:3] == 'RDG':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-RDG}}", sep = '')
    elif col_name[:3] == 'PRV':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PR}}", sep = '')
    elif col_name[:3] == 'UMP':
        print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UMP}}", sep = '')
    elif col_name[:3] == 'REG':
        if dictionary[col_name] == 'empty':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-REG}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-REG}}", sep = '')
    elif col_name[:3] == 'EXG':
        if dictionary[col_name] == 'Lutte Ouvriere' or dictionary[col_name] == 'Lutte Ouvrière':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-LO}}", sep = '')
        elif dictionary[col_name] == 'Ligue Communiste Revolutionnaire':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-LCR}}", sep = '')
        elif dictionary[col_name] == 'Nouveau Parti Anticapitaliste':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-NPA}}", sep = '')
        elif dictionary[col_name] == 'Parti Des Travailleurs':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PT}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-EXG}}", sep = '')
    elif col_name[:3] == 'DVD':
        if dictionary[col_name] == 'Mouvement Pour La France':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-MPF}}", sep = '')
        elif dictionary[col_name] == 'Centre National Des Independants Et Paysans' or dictionary[col_name] == 'Centre National Des Independants':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-CNIP}}", sep = '')
        elif dictionary[col_name] == 'Debout La Republique' or dictionary[col_name] == 'Debout La République':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DLF}}", sep = '')
        elif dictionary[col_name] == 'Parti Chrétien-Démocrate':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PCD}}", sep = '')
        elif dictionary[col_name] == 'Union Républicaine Populaire':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UPR}}", sep = '')
        elif dictionary[col_name] == 'Rassemblement Pour La France':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-RPF}}", sep = '')
        elif dictionary[col_name] == 'Union Des Démocrates Pour La République':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-UDR}}", sep = '')
        elif dictionary[col_name] == 'Rassemblement Pour La Republique':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-RPR}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DVD}}", sep = '')
    elif col_name[:3] == 'DVG':
        if dictionary[col_name] == 'empty':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DVG}}", sep = '')
        elif dictionary[col_name] == 'Socialiste Dissidente':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PS}}", sep = '')
        elif dictionary[col_name] == 'Mouvement Des Citoyens':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-MDC}}", sep = '')
        elif dictionary[col_name] == 'Energie Radicale':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PRG}}", sep = '')
        elif dictionary[col_name] == 'Mouvement Républicain Et Citoyen':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-MRC}}", sep = '')
        elif dictionary[col_name] == 'Parti Socialiste':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-PS}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DVG}}", sep = '')
    elif col_name[:3] == 'DIV':
        if 'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux' in dictionary[col_name]:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-ECO}}", sep = '')
        elif dictionary[col_name] == 'Chasse Peche Nature Et Traditions' or dictionary[col_name] == 'Chasse Peche Nature Traditions':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-CPNT}}", sep = '')
        elif dictionary[col_name] == 'Parti Occitan':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-REG}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-DIV}}", sep = '')
    elif col_name[:3] == 'EXD':
        if dictionary[col_name] == 'Mouvement National Republicain' or dictionary[col_name] == "Mnr - Contre L'Immigration-Islamisation, L'Insecurite":
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-MNR}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-EXD}}", sep = '')
    elif col_name[:3] == 'ECO':
        if dictionary[col_name] == 'Generation Ecologie':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-GE}}", sep = '')
        elif dictionary[col_name] == 'Les Verts':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-Verts}}", sep = '')
        elif dictionary[col_name] == 'Europe-Ecologie-Les Verts':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-EELV}}", sep = '')
        elif dictionary[col_name] == 'Alliance Ecologiste Indépendante':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-AEI}}", sep = '')
        elif dictionary[col_name] == 'Mouvement Ecologiste Independant' or dictionary[col_name] == 'Mouvement Écologiste Indépendant':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-MEI}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-ECO}}", sep = '')
    elif col_name[:3] == 'COM':
        if dictionary[col_name] == 'empty':
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-COM}}", sep = '')
        else:
            print("| hex", order_number, " = {{Infobox Parti politique français/couleurs|-COM}}", sep = '')
    else:
        print('error', col_name)

def partie_name(col_name, order_number):
    if col_name == 'COM':
        print("| parti", order_number, " = [[Parti communiste français|PCF]]", sep = '')
    elif col_name == 'COM2':
        print("| parti", order_number, " = [[Apparentement|app.]] [[Parti communiste français|PCF]]", sep = '')
    elif col_name == 'UFD':
        print("| parti", order_number, " = [[Union des forces démocratiques (France)|UFD]]", sep = '')
    elif col_name == 'SFIO':
        print("| parti", order_number, " = [[Section française de l'Internationale ouvrière|SFIO]]", sep = '')
    elif col_name == 'RADSOC' or col_name == 'RADICAUX GAUCHE':
        print("| parti", order_number, " = [[Parti radical (France)|RADSOC]]", sep = '')
    elif col_name == 'RADCENT':
        print("| parti", order_number, " = Radicaux centristes", sep = '')
    elif col_name == 'RADUFD':
        print("| parti", order_number, " = Radicaux de l'[[Union des forces démocratiques (France)|UFD]]", sep = '')
    elif col_name == 'UDSRMIN':
        print("| parti", order_number, " = [[Union démocratique et socialiste de la Résistance|UDSR]]", sep = '')
    elif col_name == 'UNR':
        print("| parti", order_number, " = [[Union pour la nouvelle République|UNR]]", sep = '')
    elif col_name == 'CRR':
        print("| parti", order_number, " = [[Centre républicain|CR]]", sep = '')
    elif col_name == 'DIVGAUL':
        print("| parti", order_number, " = Divers gaullistes", sep = '')
    elif col_name == 'MRP' or col_name == 'MRPVREP':
        print("| parti", order_number, " = [[Mouvement républicain populaire|MRP]]", sep = '')
    elif col_name == 'CNI':
        print("| parti", order_number, " = [[Centre national des indépendants et paysans|CNIP]]", sep = '')
    elif col_name == 'MOD':
        print("| parti", order_number, " = [[Républicains modérés|Modérés]]", sep = '')
    elif col_name == 'EXD':
        print("| parti", order_number, " = [[Extrême droite en France|EXD]]", sep = '')
    elif col_name == 'POUJ':
        print("| parti", order_number, " = [[Poujadisme|Poujadistes]]", sep = '')
    elif col_name == 'DIV':
        print("| parti", order_number, " = Divers", sep = '')
    elif col_name == 'PSU':
        print("| parti", order_number, " = [[Parti socialiste unifié (France)|PSU]]", sep = '')
    elif col_name == 'EXG':
        print("| parti", order_number, " = [[Extrême gauche en France|EXG]]", sep = '')
    elif col_name == 'UNR-UDT':
        print("| parti", order_number, " = [[Union pour la nouvelle République|UNR-UDT]]", sep = '')
    elif col_name == 'INDVREP':
        print("| parti", order_number, " = [[Fédération nationale des républicains indépendants|RI]]", sep = '')
    elif col_name == 'FGDS':
        print("| parti", order_number, " = [[Fédération de la gauche démocrate et socialiste|FGDS]]", sep = '')
    elif col_name == 'RADDROIT':
        print("| parti", order_number, " = Radicaux de droite", sep = '')
    elif col_name == 'UDR':
        print("| parti", order_number, " = [[Union des démocrates pour la République|UDR]]", sep = '')
    elif col_name == 'RALLIE' or col_name == 'CDP':
        print("| parti", order_number, " = [[Centre démocratie et progrès|CDP]]", sep = '')
    elif col_name == 'ALLREP':
        print("| parti", order_number, " = [[Alliance républicaine pour les libertés et le progrès|AR]]", sep = '')
    elif col_name == 'RIUDR':
        print("| parti", order_number, " = [[Fédération nationale des républicains indépendants|RI]]-[[Union des démocrates pour la République|UDR]]", sep = '')
    elif col_name == 'TD':
        print("| parti", order_number, " = Technique et démocratie", sep = '')
    elif col_name == 'MDR':
        print("| parti", order_number, " = [[Mouvement des réformateurs|MR]]", sep = '')
    elif col_name == 'REG':
        print("| parti", order_number, " = [[Régionalisme (politique)|REG]]", sep = '')
    elif col_name == 'DIVMAJ' or col_name == 'DVD':
        print("| parti", order_number, " = [[Divers droite|DVD]]", sep = '')
    elif col_name == 'LO':
        print("| parti", order_number, " = [[Lutte ouvrière|LO]]", sep = '')
    elif col_name == 'LCR':
        print("| parti", order_number, " = [[Ligue communiste révolutionnaire|LCR]]", sep = '')
    elif col_name == 'OCR':
        print("| parti", order_number, " = [[Organisation communiste révolutionnaire|OCR]]", sep = '')
    elif col_name == 'SOC':
        print("| parti", order_number, " = [[Parti socialiste (France)|PS]]", sep = '')
    elif col_name == 'MRG':
        print("| parti", order_number, " = [[Parti radical de gauche|MRG]]", sep = '')
    elif col_name == 'DVG':
        print("| parti", order_number, " = [[Divers gauche|DVG]]", sep = '')
    elif col_name == 'REFRAD':
        print("| parti", order_number, " = Radicaux réformateurs", sep = '')
    elif col_name == 'DIVREF':
        print("| parti", order_number, " = Divers réformateurs", sep = '')
    elif col_name == 'UDRURP':
        print("| parti", order_number, " = [[Union des démocrates pour la République|UDR]]-[[Union des républicains de progrès|URP]]", sep = '')
    elif col_name == 'RIURP':
        print("| parti", order_number, " = [[Fédération nationale des républicains indépendants|RI]]-[[Union des républicains de progrès|URP]]", sep = '')
    elif col_name == 'CDURP' or col_name == 'CDPURP':
        print("| parti", order_number, " = [[Centre démocrate (France)|CD]]-[[Union des républicains de progrès|URP]]", sep = '')
    elif col_name == 'DIVURP':
        print("| parti", order_number, " = Divers [[Union des républicains de progrès|URP]]", sep = '')
    elif col_name == 'FRONT':
        print("| parti", order_number, " = Front Autogestionnaire", sep = '')
    elif col_name == 'PSMRG':
        print("| parti", order_number, " = [[Parti socialiste (France)|PS]]-[[Parti radical de gauche|PRG]]", sep = '')
    elif col_name == 'ECO':
        print("| parti", order_number, " = [[Écologie politique|ECO]]", sep = '')
    elif col_name == 'GAULOPP':
        print("| parti", order_number, " = Gaullistes d'opposition", sep = '')
    elif col_name == 'UDF':
        print("| parti", order_number, " = [[Union pour la démocratie française|UDF]]", sep = '')
    elif col_name == 'RPR':
        print("| parti", order_number, " = [[Rassemblement pour la République|RPR]]", sep = '')
    elif col_name == 'FRN':
        print("| parti", order_number, " = [[Rassemblement national|FN]]", sep = '')
    elif col_name == 'UDF-RPR':
        print("| parti", order_number, " = [[Union pour la démocratie française|UDF]]-[[Rassemblement pour la République|RPR]]", sep = '')
    elif col_name == 'CENTDEM':
        print("| parti", order_number, " = [[Centre démocrate (France)|CD]]", sep = '')
    elif col_name == 'OCI':
        print("| parti", order_number, " = [[Organisation communiste révolutionnaire|OCI]]", sep = '')
    else:
        print('error', col_name)

def partie_name_post(col_name, order_number, dictionary):
    if col_name[:3] == 'FDG':
        print("| parti", order_number, " = [[Front de gauche (France)|FDG]]", sep = '')
    if col_name[:3] == 'RDG':
        print("| parti", order_number, " = [[Les Radicaux de gauche|RDG]]", sep = '')
    elif col_name[:5] == 'MODEM':
        print("| parti", order_number, " = [[Mouvement démocrate (France)|MODEM]]", sep = '')
    elif col_name[:3] == 'UMP':
        print("| parti", order_number, " = [[Union pour un mouvement populaire|UMP]]", sep = '')
    elif col_name[:3] == 'SOC' or col_name[:3] == 'SDC':
        print("| parti", order_number, " = [[Parti socialiste (France)|PS]]", sep = '')
    elif col_name[:5] == 'NouvC':
        print("| parti", order_number, " = [[Les Centristes|LC]]", sep = '')
    elif col_name[:3] == 'PRG' or col_name == 'RDG':
        print("| parti", order_number, " = [[Parti radical de gauche|PRG]]", sep = '')
    elif col_name[:4] == 'PSLE':
        print("| parti", order_number, " = [[Les Centristes|PSLE]]", sep = '')
    elif col_name[:3] == 'RPR':
        print("| parti", order_number, " = [[Rassemblement pour la République|RPR]]", sep = '')
    elif col_name[:3] == 'UDF':
        print("| parti", order_number, " = [[Union pour la démocratie française|UDF]]", sep = '')
    elif col_name[:3] == 'GEC':
        print("| parti", order_number, " = [[Génération écologie|GE]]", sep = '')
    elif col_name[:3] == 'VEC':
        print("| parti", order_number, " = [[Les Verts (France)|LV]]", sep = '')
    elif col_name[:3] == 'FRN':
        print("| parti", order_number, " = [[Rassemblement national|FN]]", sep = '')
    elif col_name[:3] == 'MAJ':
        print("| parti", order_number, " = [[Union pour un mouvement populaire|UMP]]", sep = '')
    elif col_name[:3] == 'PRV':
        print("| parti", order_number, " = [[Parti radical (France)|PRV]]", sep = '')
    elif col_name[:3] == 'REG':
        if dictionary[col_name] == 'empty':
            print("| parti", order_number, " = [[Régionalisme (politique)|REG]]", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    elif col_name[:3] == 'EXG':
        if dictionary[col_name] == 'empty':
            print("| parti", order_number, " = [[Extrême gauche en France|EXG]]", sep = '')
        elif dictionary[col_name] == 'Lutte Ouvriere' or dictionary[col_name] == 'Lutte Ouvrière':
            print("| parti", order_number, " = [[Lutte ouvrière|LO]]", sep = '')
        elif dictionary[col_name] == 'Ligue Communiste Revolutionnaire':
            print("| parti", order_number, " = [[Ligue communiste révolutionnaire|LCR]]", sep = '')
        elif dictionary[col_name] == 'Nouveau Parti Anticapitaliste':
            print("| parti", order_number, " = [[Nouveau Parti anticapitaliste|NPA]]", sep = '')
        elif dictionary[col_name] == 'Les Alternatifs' or dictionary[col_name] == 'Alternatifs (Solidarite, Ecologie, Gauche Alternative)':
            print("| parti", order_number, " = [[Les Alternatifs]]", sep = '')
        elif dictionary[col_name] == 'Extrême gauche':
            print("| parti", order_number, " = [[Extrême gauche en France|EXG]]", sep = '')
        elif dictionary[col_name] == 'Parti Des Travailleurs':
            print("| parti", order_number, " = [[Parti des travailleurs (France)|PT]]", sep = '')
        elif dictionary[col_name] == 'Gauche Alternative 2007':
            print("| parti", order_number, " = [[Gauche alternative 2007|GP2007]]", sep = '')
        elif dictionary[col_name] == 'Alternative Rouge Et Verte':
            print("| parti", order_number, " = [[Alternative rouge et verte|ARV]]", sep = '')
        elif dictionary[col_name] == 'Sans Etiquette':
            print("| parti", order_number, " = [[Sans étiquette|SE]]", sep = '')
        elif dictionary[col_name] == 'Solidarite Ecologie Gauche Alternative' or dictionary[col_name] == 'Solidarite, Ecologie, Gauche Alternative (Sega)':
            print("| parti", order_number, " = [[Gauche alternative 2007|SEGA]]", sep = '')
        elif dictionary[col_name] == 'Candidat D Initiative Pour Une Nouvelle Politique A Gauche':
            print("| parti", order_number, " = Candidat d'initiative pour une nouvelle politique à gauche", sep = '')
        elif dictionary[col_name] == 'Voix Des Travailleurs':
            print("| parti", order_number, " = [[Voix des travailleurs|VdT]]", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    elif col_name[:3] == 'DVD':
        if dictionary[col_name] == 'empty':
            print("| parti", order_number, " = [[Divers droite|DVD]]", sep = '')
        elif dictionary[col_name] == 'Mouvement Pour La France':
            print("| parti", order_number, " = [[Mouvement pour la France|MPF]]", sep = '')
        elif dictionary[col_name] == 'Debout La Republique' or dictionary[col_name] == 'Debout La République':
            print("| parti", order_number, " = [[Debout la France|DLR]]", sep = '')
        elif dictionary[col_name] == 'Sans Etiquette':
            print("| parti", order_number, " = [[Sans étiquette|SE]]", sep = '')
        elif dictionary[col_name] == 'Centre National Des Independants Et Paysans':
            print("| parti", order_number, " = [[Centre national des indépendants et paysans|CNIP]]", sep = '')
        elif dictionary[col_name] == 'Centre National Des Independants':
            print("| parti", order_number, " = [[Centre national des indépendants et paysans|CNI]]", sep = '')
        elif dictionary[col_name] == 'Parti Chrétien-Démocrate':
            print("| parti", order_number, " = [[VIA, la voie du peuple|PCD]]", sep = '')
        elif dictionary[col_name] == 'Union Républicaine Populaire':
            print("| parti", order_number, " = [[Union populaire républicaine (2007)|UPR]]", sep = '')
        elif dictionary[col_name] == 'Divers Droite':
            print("| parti", order_number, " = [[Divers droite|DVD]]", sep = '')
        elif dictionary[col_name] == 'La Droite Independante (Mpf)':
            print("| parti", order_number, " = [[La droite indépendante|LDI]]", sep = '')
        elif dictionary[col_name] == 'Rassemblement Pour La France':
            print("| parti", order_number, " = [[Rassemblement pour la France|RPF]]", sep = '')
        elif dictionary[col_name] == 'Union Des Démocrates Pour La République':
            print("| parti", order_number, " = [[Union des démocrates pour la République|UDR]]", sep = '')
        elif dictionary[col_name] == 'Rassemblement Pour La Republique':
            print("| parti", order_number, " = [[Rassemblement pour la République|RPR]]", sep = '')
        elif dictionary[col_name] == 'Droite Liberale Chretienne':
            print("| parti", order_number, " = [[Droite libérale-chrétienne|DLC]]", sep = '')
        elif dictionary[col_name] == 'Alternative Liberale':
            print("| parti", order_number, " = [[Alternative libérale|AL]]", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    elif col_name[:3] == 'DVG':
        if dictionary[col_name] == 'empty' or dictionary[col_name] == 'Divers Gauche':
            print("| parti", order_number, " = [[Divers gauche|DVG]]", sep = '')
        elif dictionary[col_name] == 'Pole Republicain':
            print("| parti", order_number, " = [[Pôle républicain|PR]]", sep = '')
        elif dictionary[col_name] == 'Sans Etiquette':
            print("| parti", order_number, " = [[Sans étiquette|SE]]", sep = '')
        elif dictionary[col_name] == 'Mouvement Republicain Et Citoyen':
            print("| parti", order_number, " = [[Mouvement républicain et citoyen|MRC]]", sep = '')
        elif dictionary[col_name] == 'Socialiste Dissidente':
            print("| parti", order_number, " = [[Dissidence|diss]] [[Parti socialiste (France)|PS]]", sep = '')
        elif dictionary[col_name] == 'Pour La Semaine De 4 Jours':
            print("| parti", order_number, " = [[Semaine de quatre jours|Pour la semaine de 4 jours]]", sep = '')
        elif dictionary[col_name] == 'Mouvement Des Citoyens':
            print("| parti", order_number, " = [[Mouvement des citoyens (France)|MDC]]", sep = '')
        elif dictionary[col_name] == 'Energie Radicale':
            print("| parti", order_number, " = [[Mouvement des citoyens (France)|MDC]]", sep = '')
        elif dictionary[col_name] == 'Mouvement Républicain Et Citoyen':
            print("| parti", order_number, " = [[Mouvement républicain et citoyen|MRC]]", sep = '')
        elif dictionary[col_name] == 'Parti Socialiste':
            print("| parti", order_number, " = [[Parti socialiste (France)|PS]]", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    elif col_name[:3] == 'DIV':
        if dictionary[col_name] == 'empty':
            print("| parti", order_number, " = Divers", sep = '')
        elif 'Les Nouveaux Ecologistes Du Rassemblement Nature Et Animaux' in dictionary[col_name] or dictionary[col_name] == 'Le Trefle - Les Nouveaux Ecologistes':
            print("| parti", order_number, " = [[Le Trèfle - Les nouveaux écologistes|NERNA]]", sep = '')
        elif dictionary[col_name] == 'Parti De La Loi Naturelle':
            print("| parti", order_number, " = [[Parti de la loi naturelle|PLN]]", sep = '')
        elif dictionary[col_name] == 'Sans Etiquette':
            print("| parti", order_number, " = [[Sans étiquette|SE]]", sep = '')
        elif dictionary[col_name] == 'Chasse Peche Nature Et Traditions' or dictionary[col_name] == 'Chasse Peche Nature Traditions':
            print("| parti", order_number, " = [[Le Mouvement de la ruralité|CPNT]]", sep = '')
        elif dictionary[col_name] == 'Parti Federaliste':
            print("| parti", order_number, " = [[Parti fédéraliste (France)|PF]]", sep = '')
        elif dictionary[col_name] == 'Solidarité Et Progrès' or dictionary[col_name] == 'Regions Et Peuples Solidaires':
            print("| parti", order_number, " = [[Solidarité et progrès|SP]]", sep = '')
        elif dictionary[col_name] == 'Parti Humaniste':
            print("| parti", order_number, " = [[Parti humaniste (France)|PH]]", sep = '')
        elif dictionary[col_name] == 'Rassemblement Des Contribuables Francais':
            print("| parti", order_number, " = [[Nicolas Miguet|Rassemblement des contribuables francais]]", sep = '')
        elif dictionary[col_name] == 'Parti Rachid Nekkaz':
            print("| parti", order_number, " = [[Rachid Nekkaz|Parti Rachid Nekkaz]]", sep = '')
        elif dictionary[col_name] == 'Parti Occitan':
            print("| parti", order_number, " = [[Partit occitan|PO]]", sep = '')
        elif dictionary[col_name] == 'Energies Democrates':
            print("| parti", order_number, " = [[Christian Blanc|Energies democrates]]", sep = '')
        elif dictionary[col_name] == 'Parti Des Socioprofessionnels':
            print("| parti", order_number, " = Parti des socioprofessionnels", sep = '')
        elif dictionary[col_name] == "Rassemblement Pour L'Initiative Citoyenne":
            print("| parti", order_number, " = Rassemblement pour l'initiative citoyenne", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    elif col_name[:3] == 'EXD':
        if dictionary[col_name] == 'empty':
            print("| parti", order_number, " = [[Extrême droite en France|EXD]]", sep = '')
        elif dictionary[col_name] == 'Mouvement National Republicain' or dictionary[col_name] == "Mnr - Contre L'Immigration-Islamisation, L'Insecurite	":
            print("| parti", order_number, " = [[Mouvement national républicain|MNR]]", sep = '')
        elif dictionary[col_name] == 'Union De La Droite Nationale':
            print("| parti", order_number, " = [[Union de la droite nationale|UDN]]", sep = '')
        elif dictionary[col_name] == 'Parti Anti-Sioniste':
            print("| parti", order_number, " = [[Parti antisioniste|PAS]]", sep = '')
        elif dictionary[col_name] == 'Defendons La Chasse Et Nos Traditions':
            print("| parti", order_number, " = Défendons la chasse et nos traditions", sep = '')
        elif dictionary[col_name] == 'Rassemblement Republicain Pour L Union Centriste':
            print("| parti", order_number, " = Rassemblement républicain pour l'union centriste", sep = '')
        elif dictionary[col_name] == 'Sans Etiquette':
            print("| parti", order_number, " = [[Sans étiquette|SE]]", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    elif col_name[:3] == 'ECO':
        if dictionary[col_name] == 'empty' or dictionary[col_name] == 'Ecologiste':
            print("| parti", order_number, " = [[Écologisme|ECO]]", sep = '')
        elif dictionary[col_name] == 'Generation Ecologie':
            print("| parti", order_number, " = [[Génération écologie|GE]]", sep = '')
        elif dictionary[col_name] == 'Les Verts':
            print("| parti", order_number, " = [[Les Verts (France)|LV]]", sep = '')
        elif dictionary[col_name] == 'Sans Etiquette':
            print("| parti", order_number, " = [[Sans étiquette|SE]]", sep = '')
        elif dictionary[col_name] == 'Europe-Ecologie-Les Verts':
            print("| parti", order_number, " = [[Europe Écologie Les Verts|EELV]]", sep = '')
        elif dictionary[col_name] == 'Alliance Ecologiste Indépendante':
            print("| parti", order_number, " = [[Alliance écologiste indépendante|AEI]]", sep = '')
        elif dictionary[col_name] == 'Le Trèfle - Les Nouveaux Ecologistes' or dictionary[col_name] == 'Le Trefle':
            print("| parti", order_number, " = [[Le Trèfle - Les nouveaux écologistes|Le Trèfle]]", sep = '')
        elif dictionary[col_name] == 'Mouvement Ecologiste Independant' or dictionary[col_name] == 'Mouvement Écologiste Indépendant':
            print("| parti", order_number, " = [[Mouvement écologiste indépendant|MEI]]", sep = '')
        elif dictionary[col_name] == 'Mouvement Hommes-Animaux-Nature : Mhan' or dictionary[col_name] == 'Mouvement Homme Nature Animaux':
            print("| parti", order_number, " = [[Mouvement hommes animaux nature|MHAN]]", sep = '')
        elif dictionary[col_name] == 'Citoyennete Action Participation Pour Le 21E Siecle':
            print("| parti", order_number, " = Citoyenneté action participation pour le 21{{e}} siècle", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    elif col_name[:3] == 'COM':
        if dictionary[col_name] == 'empty':
            print("| parti", order_number, " = [[Communisme|COM]]", sep = '')
        elif dictionary[col_name] == 'Parti Communiste Francais' or dictionary[col_name] == 'Candidat De Rassemblement Presente Par Le Parti Comâ­Muniste Francais' or dictionary[col_name] == 'Candidat De Rassemblement Presente Par Le Pcf' or dictionary[col_name] == 'Candidat De Rassemblement Presente Par Le Parti Communiste Francais' or dictionary[col_name] == 'Candidat Rassemblement Pcf':
            print("| parti", order_number, " = [[Parti communiste français|PCF]]", sep = '')
        else:
            print("| parti", order_number, " = ", dictionary[col_name], sep = '')
    else:
        print('error', col_name)

sys.argv = ['circo.py', '-d', 'CHARENTE-MARITIME', '-c', '5']
#on recupere les options utilisateurs 
parser = argparse.ArgumentParser(description="Gap filling programms")
#recupere le fichier comportant les reads
parser.add_argument("-d", "--departement", required=True)
#recupere le fichier comportant le start et stop
parser.add_argument("-c", "--circo", required=True, type=int)
param = parser.parse_args()

##
# 1958
##

t1958a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1958t1_circ.xls', index_col=None)
t1958b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1958t2_circ.xls', index_col=None)

t1958b_circo = find_circo(t1958b, param.departement, param.circo)

monotour = exist_second(t1958b_circo)
print("| titre = Résultats des élections législatives des 23 et 30 novembre 1958 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 23/11/1958 par circonscription, cdsp_legi1958t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1958a_circo = find_circo(t1958a, param.departement, param.circo)
premier_tour(t1958a_circo)
subseta = t1958a_circo.iloc[:,7:t1958a_circo.size]
subsetb = t1958b_circo.iloc[:,8:t1958b_circo.size]
corps(subseta, subsetb, monotour, t1958b_circo)

##
# 1962
##

t1962a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1962t1_circ.xls', index_col=None)
t1962b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1962t2_circ.xls', index_col=None)

t1962b_circo = find_circo(t1962b, param.departement, param.circo)

monotour = exist_second(t1962b_circo)
print("| titre = Résultats des élections législatives des 18 et 25 novembre 1962 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 18/11/1962 par circonscription, cdsp_legi1962t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1962a_circo = find_circo(t1962a, param.departement, param.circo)
premier_tour(t1962a_circo)
subseta = t1962a_circo.iloc[:,7:t1962a_circo.size]
subsetb = t1962b_circo.iloc[:,8:t1962b_circo.size]
corps(subseta, subsetb, monotour, t1962b_circo)

##
# 1967
##

t1967a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1967t1_circ.xls', index_col=None)
t1967b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1967t2_circ.xls', index_col=None)

t1967b_circo = find_circo(t1967b, param.departement, param.circo)

monotour = exist_second(t1967b_circo)
print("| titre = Résultats des élections législatives des 5 et 12 mars 1967 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 05/03/1967 par circonscription, cdsp_legi1967t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1967a_circo = find_circo(t1967a, param.departement, param.circo)
premier_tour(t1967a_circo)
subseta = t1967a_circo.iloc[:,7:t1967a_circo.size]
subsetb = t1967b_circo.iloc[:,8:t1967b_circo.size]
corps(subseta, subsetb, monotour, t1967b_circo)

##
# 1968
##

t1968a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1968t1_circ.xls', index_col=None)
t1968b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1968t2_circ.xls', index_col=None)

t1968b_circo = find_circo(t1968b, param.departement, param.circo)

monotour = exist_second(t1968b_circo)
print("| titre = Résultats des élections législatives des 23 et 30 juin 1968 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 23/06/1968 par circonscription, cdsp_legi1968t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1968a_circo = find_circo(t1968a, param.departement, param.circo)
premier_tour(t1968a_circo)
subseta = t1968a_circo.iloc[:,7:t1968a_circo.size]
subsetb = t1968b_circo.iloc[:,8:t1968b_circo.size]
corps(subseta, subsetb, monotour, t1968b_circo)

##
# 1973
##

t1973a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1973t1_circ.xls', index_col=None)
t1973b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1973t2_circ.xls', index_col=None)

t1973b_circo = find_circo(t1973b, param.departement, param.circo)

monotour = exist_second(t1973b_circo)
print("| titre = Résultats des élections législatives des 4 et 11 mars 1973 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 11/03/1973 par circonscription, cdsp_legi1973t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1973a_circo = find_circo(t1973a, param.departement, param.circo)
premier_tour(t1973a_circo)
subseta = t1973a_circo.iloc[:,7:t1973a_circo.size]
subsetb = t1973b_circo.iloc[:,8:t1973b_circo.size]
corps(subseta, subsetb, monotour, t1973b_circo)

##
# 1978
##

t1978a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1978t1_circ.xls', index_col=None)
t1978b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1978t2_circ.xls', index_col=None)

t1978b_circo = find_circo(t1978b, param.departement, param.circo)

monotour = exist_second(t1978b_circo)
print("| titre = Résultats des élections législatives des 12 et 18 mars 1978 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 12/03/1978 par circonscription, cdsp_legi1978t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1978a_circo = find_circo(t1978a, param.departement, param.circo)
premier_tour(t1978a_circo)
subseta = t1978a_circo.iloc[:,7:t1978a_circo.size]
subsetb = t1978b_circo.iloc[:,8:t1978b_circo.size]
corps(subseta, subsetb, monotour, t1978b_circo)

##
# 1981
##

t1981a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1981t1_circ.xls', index_col=None)
t1981b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1981t2_circ.xls', index_col=None)

t1981b_circo = find_circo(t1981b, param.departement, param.circo)

monotour = exist_second_post(t1981b_circo)
print("| titre = Résultats des élections législatives des 14 et 21 juin 1981 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 14/06/1981 par circonscription, cdsp_legi1981t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1981a_circo = find_circo(t1981a, param.departement, param.circo)
premier_tour(t1981a_circo)
subseta = t1981a_circo.iloc[:,6:t1981a_circo.size]
subsetb = t1981b_circo.iloc[:,7:t1981b_circo.size]
corps(subseta, subsetb, monotour, t1981b_circo)

##
# 1988
##

t1988a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1988t1_circ.xls', index_col=None)
t1988b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1988t2_circ.xls', index_col=None)

t1988b_circo = find_circo(t1988b , param.departement, param.circo)

monotour = exist_second_post(t1988b_circo)
print("| titre = Résultats des élections législatives des 5 et 12 juin 1988 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 05/06/1988 par circonscription, cdsp_legi1988t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1988a_circo = find_circo(t1988a, param.departement, param.circo)
premier_tour(t1988a_circo)
corps_post(t1988a_circo, t1988b_circo, monotour)

##
# 1993
##

t1993a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1993t1_circ.xls', index_col=None)
t1993b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1993t2_circ.xls', index_col=None)

t1993b_circo = find_circo(t1993b , param.departement, param.circo)

monotour = exist_second_post(t1993b_circo)
print("| titre = Résultats des élections législatives des 21 et 12 mars 1993 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 21/03/1993 par circonscription, cdsp_legi1993t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1993a_circo = find_circo(t1993a, param.departement, param.circo)
premier_tour(t1993a_circo)
corps_post(t1993a_circo, t1993b_circo, monotour)

##
# 1997
##

t1997a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1997t1_circ.xls', index_col=None)
t1997b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi1997t2_circ.xls', index_col=None)

t1997b_circo = find_circo(t1997b , param.departement, param.circo)

monotour = exist_second_post(t1997b_circo)
print("| titre = Résultats des élections législatives des 25 et 12 mai 1997 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 25/05/1997 par circonscription, cdsp_legi1997t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t1997a_circo = find_circo(t1997a, param.departement, param.circo)
premier_tour(t1997a_circo)
corps_post(t1997a_circo, t1997b_circo, monotour)

##
# 2002
##

t2002a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2002t1_circ.xls', index_col=None)
t2002b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2002t2_circ.xls', index_col=None)

t2002b_circo = find_circo(t2002b , param.departement, param.circo)

monotour = exist_second_post(t2002b_circo)
print("| titre = Résultats des élections législatives des 9 et 12 juin 2002 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 09/06/2002 par circonscription, cdsp_legi2002t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t2002a_circo = find_circo(t2002a, param.departement, param.circo)
premier_tour(t2002a_circo)
corps_post(t2002a_circo, t2002b_circo, monotour)

##
# 2007
##

t2007a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2007t1_circ.xls', index_col=None)
t2007b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2007t2_circ.xls', index_col=None)

t2007b_circo = find_circo(t2007b , param.departement, param.circo)

monotour = exist_second_post(t2007b_circo)
print("| titre = Résultats des élections législatives des 10 et 12 juin 2007 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 10/06/2007 par circonscription, cdsp_legi2007t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t2007a_circo = find_circo(t2007a, param.departement, param.circo)
premier_tour(t2007a_circo)
corps_post(t2007a_circo, t2007b_circo, monotour)

##
# 2012
##

t2012a = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2012t1_circ.xlsx', index_col=None)
t2012b = pd.read_excel('D:\Downloads\legis\LEGISLATIVES_1958-2012-xls - Copie\cdsp_legi2012t2_circ.xlsx', index_col=None)

t2012b_circo = find_circo(t2012b , param.departement, param.circo)

monotour = exist_second_post(t2012b_circo)
print("| titre = Résultats des élections législatives des 10 et 17 juin 2012 de la ", param.circo, "e circonscription du ", param.departement.title(), sep = '')
print("| references = <ref>Résultats des élections législatives françaises premier tour du 10/06/2012 par circonscription, cdsp_legi2012t1_circ.xls [fichier informatique], Banque de Données Socio-Politiques, Grenoble [producteur], Centre de Données Socio-politiques [diffuseur], février 2009.</ref>")

t2012a_circo = find_circo(t2012a, param.departement, param.circo)
premier_tour(t2012a_circo)
corps_post(t2012a_circo, t2012b_circo, monotour)