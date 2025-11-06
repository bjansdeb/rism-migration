from lxml import etree
from lxml.etree import tostring
import sys
import re

"""Version with indication"""
"""Spécificité, les 852c RISM contiennent les 001 Koha et se répètent entre papas et enfants"""
"""Les 852c doivent être récupérés et placés en 001 avec une numérotation correspondant au numéro d'index des 774"""
"""Les records sont visibles sur Koha"""
"""773 information concerning the host item for the constituent unit described in the record"""
"""774 child records ID"""

def main():
    count = 0
    c_001_values = {}
    array_852_c = {}
    occurences_852_c = []
    etree.register_namespace("marc", "http://www.loc.gov/MARC21/slim")
    with_indication = etree.iterparse("with_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")
    fixed_with_indication = open("final_with_indication.xml","w+", encoding= "utf-8")

    # fixed_001 = open("001fixed_wi_wdp2wave.xml","w+", encoding= "utf-8")
    print("launched")
    try:
        """1ère itération pour découvrir les papas et les enfants et les 852c"""
        for event, elt in with_indication:
            if event=="end":
                count +=1
                datafields={}
                subfields_773 ={}
                subfields_774 =[]
                c_001_value = ""

                for controlfield in elt.findall("{http://www.loc.gov/MARC21/slim}controlfield"):  
                    if controlfield.get("tag") == "001":
                        if re.findall("^00000", controlfield.text):
                            c_001_value = re.sub("^00000", "", controlfield.text)
                        else:
                            c_001_value = controlfield.text

                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") =="773":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="w":
                                if re.findall("^00000", subfield.text):
                                    subfield.text = re.sub("^00000", "", subfield.text)                                     
                                subfields_773.update({"w": subfield.text})
                                datafields.update({"773": subfields_773})
                                c_001_values.update({c_001_value : datafields})
                        # print(c_001_values[c_001_value])
                                                
                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") =="774":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="w":
                                if re.findall("^00000", subfield.text):
                                    subfield.text = re.sub("^00000", "", subfield.text)     
                                subfields_774.append(subfield.text)
                                datafields.update({"774": subfields_774})
                                c_001_values.update({c_001_value : datafields})
                        # print(c_001_values[c_001_value])

                    if datafield.get("tag") == "852":
                        subfields_852 = {}
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a" and subfield.text == "B-Bc":
                                subfields_852.update({'a' : subfield.text})
                            if subfield.get("code") == "c"  :
                               subfields_852.update({'c' : subfield.text}) 
                        if 'a' in subfields_852 and 'c' in subfields_852:
                            #datafields.update({"852": subfields_852})
                            #values_852.append(subfields_852["c"])
                            array_852_c.update({c_001_value: subfields_852["c"]})
                            occurences_852_c.append(subfields_852["c"])

                #array_852_c.update({c_001_value : values_852})
                c_001_values.update({c_001_value : datafields})
                c_001_value = ""
                elt.clear()

        #print(c_001_values)
        print("total de base :", count)
        #print(array_852_c)
        parents_and_neutral = {}
        with_indication_2round = etree.iterparse("with_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")
        for evt, el in with_indication_2round:
            if evt =="end":
                for controlfield in el.findall("{http://www.loc.gov/MARC21/slim}controlfield"):
                    if controlfield.get("tag") == "001":
                        if re.findall("^00000", controlfield.text):
                            controlfield.text = re.sub("^00000", "", controlfield.text) 
                        """773 = cote du papa pour les enfants, 774, les cotes enfants pour le papa"""
                            #print(ancien_001, controlfield.text, "est papa")
                        """Si on est en présence d'un 001 avec un 773 dans ses clés, c'est un enfant ne fait rien"""
                        if "773" in c_001_values[controlfield.text].keys():                         
                            ...
                            """Autrement, ça veut dire que c'est un papa et qu'on peut lui donner sa cote 852c (ris +1 chez no indication)"""
                        else :
                            if controlfield.text in array_852_c:
                                ancien_001 = controlfield.text
                                controlfield.text = array_852_c[controlfield.text]
                                parents_and_neutral[ancien_001] = controlfield.text                                    

                el.clear()

        #print("parents and neutral",parents_and_neutral)
        with_indication_3round = etree.iterparse("with_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")


        """3e passage pour remplir le tableau enfant"""
        children = {}
        for evt, elt in with_indication_3round:
            if evt =="end":
                tag_values = []
                values_593a = []
                identifier = ""

                for controlfield in elt.findall("{http://www.loc.gov/MARC21/slim}controlfield"):
                    if controlfield.get("tag") == "001":
                        if re.findall("^00000", controlfield.text):
                            controlfield.text = re.sub("^00000", "", controlfield.text)
                            # if controlfield.text in array_852_c:
                            #     clue = array_852_c[controlfield.text]
                            #     """vient vérifier si la cote de l'enfant contient / ou ( et donc éviter de la changer"""
                            #     if re.search(r"\/|\(|\[", clue):
                            #         #print(clue, "contient / ou (")
                            #         children[controlfield.text] = clue + "cdcerf"
                                # else:                                                     
                        """autrement on crée la cote enfant comme on a fait avec les [no indication]"""
                        """773 = cote du papa pour les enfants, 774, les cotes enfants pour le papa"""
                        if controlfield.text in c_001_values and "773" in c_001_values[controlfield.text].keys():
                            dad = c_001_values[controlfield.text]["773"]["w"] #on va chercher la valeur du papa
                            #print(dad)
                            if dad in parents_and_neutral:
                                daddy_notation = parents_and_neutral[dad]
                                if dad in c_001_values and controlfield.text in c_001_values[dad]["774"]: 
                                    index = c_001_values[dad]["774"].index(controlfield.text) + 1                         
                                    child_001 = daddy_notation + " onderdeel-" +str(index)
                                    children[controlfield.text] = child_001

        with_indication_4round = etree.iterparse("with_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")

        duplicates_852c = {}
        for evt, elt in with_indication_4round:
            if evt =="end":
                tag_values = []
                values_593a = []
                identifier = ""
                c_001_value = ""
                for controlfield in elt.findall("{http://www.loc.gov/MARC21/slim}controlfield"):
                    if controlfield.get("tag") == "001":
                        if re.findall("^00000", controlfield.text):
                            controlfield.text = re.sub("^00000", "", controlfield.text)
                        c_001_value = controlfield.text #pour récupération anciennce cote                        
                        """773 = cote du papa pour les enfants, 774, les cotes enfants pour le papa"""
                        if "773" in c_001_values[controlfield.text].keys():
                            dad = c_001_values[controlfield.text]["773"]["w"]
                            if dad in parents_and_neutral:
                                daddy_notation = parents_and_neutral[dad]
                                if dad in c_001_values and controlfield.text in c_001_values[dad]["774"]:
                                    index = c_001_values[dad]["774"].index(controlfield.text) + 1                         
                                    child_001 = daddy_notation + " onderdeel-" +str(index)
                                    controlfield.text = child_001                                
                                    identifier = daddy_notation + "-" +str(index) #avant controlfield.text
                            else :                                
                                if controlfield.text in array_852_c:
                                    ancien_value = controlfield.text
                                    controlfield.text = array_852_c[controlfield.text]
                                    if controlfield.text not in duplicates_852c:
                                        duplicates_852c.update({controlfield.text : 1}) 
                                        #ajouter un if else ici en fonction de si le nombre d'occurences de 852c est supérieur à 1 ou non
                                        if occurences_852_c.count(controlfield.text) == 1:
                                            controlfield.text = array_852_c[ancien_value]
                                        else : 
                                            controlfield.text = array_852_c[ancien_value] + " onderdeel-" + str(duplicates_852c[controlfield.text])
                                    elif controlfield.text in duplicates_852c and ancien_value in array_852_c:
                                        # key = controlfield.text
                                        duplicates_852c[controlfield.text] +=1
                                        controlfield.text = array_852_c[ancien_value] + " onderdeel-" + str(duplicates_852c[controlfield.text])

                        elif controlfield.text in parents_and_neutral:
                            controlfield.text = parents_and_neutral[controlfield.text]
                            identifier = controlfield.text

                tag_240_a, tag_245_a, tag_240_k, tag_240_m, tag_240_n, tag_240_r, tag_240_0 = "","", "", "", "", "", ""

                #Ajoute le 040 quand il n'est pas là #obligatoire et casse couille dans Koha
                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") == "040":
                        tag_value = "040"
                        c_exist = False
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="c":
                                c_exist = True
                                pass
                        if c_exist == False:
                            #crée un subfield c à 040 si celui-ci n'est pas présent
                            new_subfield_c = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="c")
                            datafield.append(new_subfield_c)
                            new_subfield_c.text = "BE-BxLRC"
                        if tag_value not in tag_values:
                            tag_values.append(tag_value)

                #on récupère les 240a et 245a et on les intervertit 
                    if datafield.get("tag") =="240":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="a":
                                tag_240_a = subfield.text
                            if subfield.get("code") =="k":
                                tag_240_k = subfield.text
                                subfield.text = ""
                            if subfield.get("code") =="m":
                                tag_240_m = subfield.text
                                subfield.text =""
                            if subfield.get("code") == "n":
                                tag_240_n = subfield.text
                                subfield.text =""
                            if subfield.get("code") == "r":
                                tag_240_r = subfield.text
                                subfield.text = ""
                            # if subfield.get("code") == "0":
                            #     tag_240_0 = subfield.text    
                                                                                                                                                          
                    if datafield.get("tag") =="245":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") == "a":
                                tag_245_a = subfield.text
                #print(values_040_subfields)
                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") =="240":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="a":
                                subfield.text = tag_245_a
                    if datafield.get("tag") =="245":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") == "a":
                                if tag_240_a != "" and tag_240_m != "":
                                    united_240_am = tag_240_a + "," + tag_240_m 
                                    subfield.text = united_240_am
                                else:
                                    subfield.text = tag_240_a

                    #concaténation de 240n avec 383b si 383b existe, sinon crée une balise 383b avec le contenu de 240n
                    if tag_240_n != "":
                        if datafield.get("tag") == "383":
                            tag_value = "383"
                            b_exist = False
                            for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                                if subfield.get("code") == "b":
                                    united_383 = subfield.text + ", " + tag_240_n
                                    subfield.text = united_383
                                    b_exist = True
                            if b_exist == True:
                                new_subfield_b = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="b")
                                datafield.append(new_subfield_b)
                                new_subfield_b.text = tag_240_n                                   
                            if tag_value not in tag_values:    
                                tag_values.append("383")
                    

                    #vérifie quel type de document est mentionné en 593a pour placer MP ou MM en 940c
                    if datafield.get("tag") =="593":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="a":
                                if subfield.text not in values_593a:
                                    values_593a.append(subfield.text)
                document_kind = "" #utilisé pour les exemplaires
                if "Manuscript copy" in values_593a:
                    new_tag_942c = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="942", ind1=" ", ind2=" ")
                    elt.insert(-1, new_tag_942c)
                    new_subfield_c = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="c")
                    new_tag_942c.append(new_subfield_c)
                    new_subfield_c.text = "MM"
                    document_kind = new_subfield_c.text
                    new_subfield_n = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="n")
                    new_tag_942c.append(new_subfield_n)
                    new_subfield_n.text = "1"                    
                elif "Print" in values_593a:
                    new_tag_942c = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="942", ind1=" ", ind2=" ")
                    elt.insert(-1, new_tag_942c)
                    new_subfield_c = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="c")
                    new_tag_942c.append(new_subfield_c)
                    new_subfield_c.text = "MP"
                    document_kind = new_subfield_c.text       
                    new_subfield_n = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="n")
                    new_tag_942c.append(new_subfield_n)
                    new_subfield_n.text = "1"                                                                     
                else:
                    new_tag_942c = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="942", ind1=" ", ind2=" ")
                    elt.insert(-1, new_tag_942c)
                    new_subfield_c = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="c")
                    new_tag_942c.append(new_subfield_c)
                    new_subfield_c.text = "RI"
                    new_subfield_n = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="n")
                    new_tag_942c.append(new_subfield_n)
                    new_subfield_n.text = "1"                     
                    document_kind = "RI" #par sécurité, j'ajoute cette valeur par défaut au cas où 593a est vide (si vide peut faire buguer les exemplaires)
                # new_subfield_n = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="n")
                # new_tag_942.append(new_subfield_n)
                # new_subfield_n.text = "1"                        
                    # pass

                # new_subfield_n = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="n")
                # new_tag_942.append(new_subfield_n)
                # new_subfield_n.text = "1"                

                values_593a.clear()
                
                """Ajout de balise"""
                "ajout de 040 si n'existe pas dans RISM ; 040 est unique"
                if "040" not in tag_values:
                    new_tag_040 = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="040", ind1=" ", ind2=" ")
                    elt.insert(-1, new_tag_040)                    
                    new_subfield_c = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="c")
                    new_tag_040.append(new_subfield_c)
                    new_subfield_c.text = "BE-BxLRC"

                if "383" not in tag_values:
                    new_tag_383b = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="383", ind1=" ", ind2=" ")
                    elt.insert(-1, new_tag_383b)
                    new_subfield_b = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="b")
                    new_tag_383b.append(new_subfield_b)
                    new_subfield_b.text = tag_240_n      

                "ajout d'une balise 300a avec ancienne valeur 240_k"
                "300a n'est pas unique dans RISM"
                if tag_240_k != "":
                    new_tag_300e = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="300", ind1=" ", ind2=" ")
                    elt.insert(-1, new_tag_300e)
                    new_subfield_e = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="e")
                    new_tag_300e.append(new_subfield_e)
                    new_subfield_e.text = tag_240_k


                """ajout d'une balise 382a avec la valeur de 240m"""
                """382 n'est pas utilisé dans RISM"""
                new_tag_382 = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="382", ind1=" ", ind2=" ")
                elt.insert(-1,new_tag_382)
                tag_382_subfield_a = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="a")
                new_tag_382.append(tag_382_subfield_a)
                tag_382_subfield_a.text = tag_240_m

                "ajout d'une balise 384a avec ancienne valeur 240_r"
                if tag_240_r != "":
                    new_tag_384a = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="384", ind1=" ", ind2=" ")
                    elt.insert(-1, new_tag_384a)
                    new_subfield_a = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="a")
                    new_tag_384a.append(new_subfield_a)
                    new_subfield_a.text = tag_240_r
              
                """ajout d'une balise 500a avec l'ancien titre"""
                """500 n'est pas unique"""
                new_tag_500 = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="500", ind1=" ", ind2=" ")
                elt.insert(-1,new_tag_500)
                new_subfield_a = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="a")
                new_tag_500.append(new_subfield_a)
                c_001_refined = c_001_value
                if re.findall("^00000", c_001_refined):
                    c_001_refined = re.sub("^00000", "", c_001_refined)
                tag_852_c_value = array_852_c[c_001_refined]
                new_subfield_a.text = f"This record comes from RISM record no. {c_001_refined} with shelfmark bbc 852c {tag_852_c_value} indicated"
                c_001_refined, tag_852_c_value = "", ""

                """traitement ajout du nouvel identifant en 773 et 774 si correspondant à l'ancien 001_RISM"""
                tag_773_w, new_tag_773w = [], []            
                tag_774_w, new_tag_774w = [], []
                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") =="773":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="w":
                                if re.findall("^00000", subfield.text):
                                    subfield.text = re.sub("^00000", "", subfield.text)     
                                if subfield.text in parents_and_neutral: #si la valeur de 773w est présente dans le tableau des anciens 001
                                    # print(subfield.text, records[subfield.text])
                                    tag_773_w.append(subfield.text)
                                    subfield.text = parents_and_neutral[subfield.text]
                                    new_tag_773w.append(subfield.text)
                                else:
                                    subfield.text = "Rism record n°: " + subfield.text

                    """Traitement des enfants renseignés, précise qu'il s'agit d'un numéro RISM si n'est pas présent dans le set"""
                    if datafield.get("tag") =="774":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") == "w":
                                if re.findall("^00000", subfield.text):
                                    subfield.text = re.sub("^00000", "", subfield.text)                                     
                                if subfield.text in children:
                                    #print(subfield.text, records[subfield.text])
                                    tag_774_w.append(subfield.text)
                                    subfield.text = children[subfield.text] 
                                    new_tag_774w.append(subfield.text)
                                else:
                                    subfield.text = "Rism record n°: " + subfield.text

                """942n à valeur 1 rend invisible la notice à l'OPAC"""
                new_tag_942 = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="942", ind1=" ", ind2=" ")
                elt.insert(-1,new_tag_942)
                new_subfield_n = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="n")
                new_tag_942.append(new_subfield_n)
                new_subfield_n.text = "1"

                """permet d'ajouter un exemplaire"""
                new_tag_952 = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="952", ind1=" ", ind2=" ")
                elt.insert(-1,new_tag_952)    
                new_subfield_0 = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="0")
                new_tag_952.append(new_subfield_0)
                new_subfield_0.text = "0"
                new_subfield_1 = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="1")
                new_tag_952.append(new_subfield_1)
                new_subfield_1.text = "0"                
                new_subfield_4 = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="4")
                new_tag_952.append(new_subfield_4)
                new_subfield_4.text = "0"                
                new_subfield_6 = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="6")
                new_tag_952.append(new_subfield_6)
                new_subfield_6.text = identifier
                new_subfield_7 = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="7")
                new_tag_952.append(new_subfield_7)
                new_subfield_7.text = "-2"  #on site consultation              
                new_subfield_952_a = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="a")
                new_tag_952.append(new_subfield_952_a)
                new_subfield_952_a.text= "B-Bc"
                new_subfield_952_b = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="b")
                new_tag_952.append(new_subfield_952_b)
                new_subfield_952_b.text= "B-Bc"
                new_subfield_952_o = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="o")
                new_tag_952.append(new_subfield_952_o)
                new_subfield_952_o.text= identifier
                new_subfield_952_p = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="p")
                new_tag_952.append(new_subfield_952_p)
                new_subfield_952_p.text= identifier                
                new_subfield_952_y = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="y")
                new_tag_952.append(new_subfield_952_y)
                new_subfield_952_y.text= document_kind                                                                           
                xml_output = tostring(elt, encoding="unicode")


                fixed_with_indication.write(str(xml_output))                                     
                tag_values.clear()

                elt.clear()
        print(duplicates_852c)

        """Securité"""
        if count > 60000:
            sys.exit("Too long script")
    except FileNotFoundError:
        print("file not found")

if __name__ == "__main__":
    main()