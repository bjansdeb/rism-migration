from lxml import etree
from lxml.etree import tostring
import sys
import re

"""place les 852c en 001 controlfield, stocke les anciens 001 control field de RISM dans 500a, traite les papas renseignés en 774w"""
"""773 information concerning the host item for the constituent unit described in the record"""
"""774 child records ID"""

def main():
    count = 0
    parsed_count = 0
    c_001_values = {}
    etree.register_namespace("marc", "http://www.loc.gov/MARC21/slim")
    no_indication = etree.iterparse("no_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")
    fixed_no_indication = open("final_no_indication.xml","w+", encoding= "utf-8")

    # fixed_001 = open("001fixed_wi_wdp2wave.xml","w+", encoding= "utf-8")
    print("launched")
    try:
        """1ère itération pour découvrir les papas et les enfants"""
        for event, elt in no_indication:
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

                c_001_values.update({c_001_value : datafields})
                c_001_value = ""
                elt.clear()


        """Exemples de données formatées en c_001_values"""
        """'706000654': {'774': {'w-1': '706000655', 'w-2': '706000656', 'w-3': '706000657', 'w-4': '706000658', 'w-5': '706000659', 'w-6': '706000660', 
        'w-7': '706000661', 'w-8': '706000662', 'w-9': '706000663', 'w-10': '706000664', 
        'w-11': '706000665', 'w-12': '706000666', 'w-13': '706000667', 'w-14': '706000668', 'w-15': '706000669', 
        'w-16': '706000670', 'w-17': '706000671', 'w-18': '706000672', 'w-19': '706000673', 'w-20': '706000674', 'w-21': '706000675', 'w-22': '706000676', 
        'w-23': '706000677', 'w-24': '706000678', 'w-25': '706000679', 'w-26': '706000680', 'w-27': '706000681', 'w-28': '706000682', 'w-29': '706000683', 
        'w-30': '706000684', 'w-31': '706000685', 'w-32': '706000686', 'w-33': '706000687', 'w-34': '706000688'}, '852': {'a': 'B-Bc', 'c': '27919'}}, 
        '706000655': {'852': {'a': 'B-Bc', 'c': '27919'}}, '706000656': {'852': {'a': 'B-Bc', 'c': '27919'}}, '706000657': {'852': {'a': 'B-Bc', 'c': '27919'}}"""


        #print(c_001_values)

        print("total de base :", count)
        print("parsed records :", parsed_count)
        parents_and_neutral = {}
        no_indication_2round = etree.iterparse("no_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")
        record_number = 0
        for evt, el in no_indication_2round:
            if evt =="end":
                for controlfield in el.findall("{http://www.loc.gov/MARC21/slim}controlfield"):
                    if controlfield.get("tag") == "001":
                        if re.findall("^00000", controlfield.text):
                            controlfield.text = re.sub("^00000", "", controlfield.text)
                        
                        """773 = cote du papa pour les enfants, 774, les cotes enfants pour le papa"""
                            #print(ancien_001, controlfield.text, "est papa")
                        if "773" in c_001_values[controlfield.text].keys():                         
                            ...
                        else :
                            record_number +=1
                            ancien_001 = controlfield.text
                            controlfield.text = "RIS-" + str("{:05d}".format(record_number))
                            parents_and_neutral[ancien_001] = controlfield.text                                    
                            #print(ancien_001, controlfield.text, "n'est ni l'un ni l'autre")
                el.clear()

                            # dad = c_001_values[controlfield.text]["773"]["w"]
                            # # print(dad)
                            # """on va chercher les cotes enfants du papa et si la cote enfant est dedans on lui adjoint le numéro"""
                            # if dad in c_001_values:
                            #     index = c_001_values[dad]["774"].index(controlfield.text) + 1
        no_indication_3round = etree.iterparse("no_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")


        """3e passage pour remplir le tableau enfant"""
        children = {}
        for evt, elt in no_indication_3round:
            if evt =="end":
                tag_values = []
                values_593a = []
                identifier = ""

                for controlfield in elt.findall("{http://www.loc.gov/MARC21/slim}controlfield"):
                    if controlfield.get("tag") == "001":
                        if re.findall("^00000", controlfield.text):
                            controlfield.text = re.sub("^00000", "", controlfield.text)                        
                        """773 = cote du papa pour les enfants, 774, les cotes enfants pour le papa"""
                        if "773" in c_001_values[controlfield.text].keys():
                            dad = c_001_values[controlfield.text]["773"]["w"]
                            daddy_notation = parents_and_neutral[dad]
                            if dad in c_001_values and controlfield.text in c_001_values[dad]["774"]:
                                index = c_001_values[dad]["774"].index(controlfield.text) + 1                         
                                child_001 = daddy_notation + " onderdeel-" +str(index)
                                children[controlfield.text] = child_001 

        no_indication_4round = etree.iterparse("no_indication_wdp2wave.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")


        for evt, elt in no_indication_4round:
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
                            daddy_notation = parents_and_neutral[dad]
                            if dad in c_001_values and controlfield.text in c_001_values[dad]["774"]:
                                index = c_001_values[dad]["774"].index(controlfield.text) + 1                         
                                child_001 = daddy_notation + " onderdeel-" +str(index)
                                controlfield.text = child_001                                
                                identifier = daddy_notation + "-" +str(index) #avant controlfield.text

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
                new_subfield_a.text = f"This record comes from RISM record no. {c_001_refined} with no shelfmark indicated"
                c_001_refined = ""

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
                # new_tag_942 = etree.Element("{http://www.loc.gov/MARC21/slim}datafield", tag="942", ind1=" ", ind2=" ")
                # elt.insert(-1,new_tag_942)
                # new_subfield_n = etree.Element("{http://www.loc.gov/MARC21/slim}subfield", code="n")
                # new_tag_942.append(new_subfield_n)
                # new_subfield_n.text = "1"

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

                fixed_no_indication.write(str(xml_output))                                     
                tag_values.clear()

                elt.clear()


        """Securité"""
        if count > 60000:
            sys.exit("Too long script")
    except FileNotFoundError:
        print("file not found")

if __name__ == "__main__":
    main()