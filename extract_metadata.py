from lxml import etree
from lxml.etree import tostring
import sys
import xlsxwriter


def main():
    count = 0
    etree.register_namespace("marc", "http://www.loc.gov/MARC21/slim")
    no_indication = etree.iterparse("final_with_indication.xml", events={"start", "end"}, tag = "{http://www.loc.gov/MARC21/slim}record")
    # csv_file = open("852c.csv", "w+", newline="")
    # csv_writer = csv.writer(csv_file)
    workbook = xlsxwriter.Workbook('metadata_with_indication_cleaned.xlsx')
    worksheet = workbook.add_worksheet()
    print("launched")

    try:
        for event, elt in no_indication:
            if event=="end":
                count +=1
                a = "A" + str(count)
                b = "B" + str(count)
                c = "C" + str(count)
                d = "D" + str(count)
                e = "E" + str(count)
                f = "F" + str(count)
                g = "G" + str(count)
                h = "H" + str(count)
                i = "I" + str(count)
                j = "J" + str(count)
                k = "K" + str(count)
                l = "L" + str(count)
                m = "M" + str(count)
                n = "N" + str(count)
                o = "O" + str(count)
                p = "P" + str(count)
                q = "Q" + str(count)
                r = "R" + str(count)
                s = "S" + str(count)
                t = "T" + str(count)
                u = "U" + str(count)
                v = "V" + str(count)


                """heading : controlfield 001, 100a, 240a, 240k, 240m, 240n, 240r, 245a, 260, 300e, 383b, 384a, 773w, 774w"""
                for controlfield in elt.findall("{http://www.loc.gov/MARC21/slim}controlfield"):  
                    if controlfield.get("tag") == "001":
                        worksheet.write(a, controlfield.text)
                                                
                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") == "100":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a":
                                worksheet.write(b, subfield.text)                    
                    if datafield.get("tag") == "240":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a":
                                worksheet.write(c, subfield.text)
                            if subfield.get("code") == "k":
                                worksheet.write(d, subfield.text)
                            if subfield.get("code") == "m":
                                worksheet.write(e, subfield.text)
                            if subfield.get("code") == "n":
                                worksheet.write(f, subfield.text)
                            if subfield.get("code") == "r":
                                worksheet.write(g, subfield.text)                                                                                                
                    if datafield.get("tag") == "245":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a":
                                worksheet.write(h, subfield.text)       

                    if datafield.get("tag") == "260":
                        tag_260 = {}
                        subfields = []
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            subfields.append(subfield.text)
                        tag_260 = {"260": subfields}
                        worksheet.write(i, str(tag_260["260"]))
                        subfields.clear()
                        tag_260.clear()

                    if datafield.get("tag") == "300":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "e":
                                worksheet.write(j, subfield.text)   
                    if datafield.get("tag") == "383":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "b":
                                worksheet.write(k, subfield.text)  
                    if datafield.get("tag") == "384":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a":
                                worksheet.write(l, subfield.text)
                    if datafield.get("tag") == "500":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a":
                                worksheet.write(o, subfield.text)
                    if datafield.get("tag") == "040":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "c":
                                worksheet.write(p, subfield.text)
                    if datafield.get("tag") == "040":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "c":
                                worksheet.write(p, subfield.text)
                    if datafield.get("tag") == "952":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "7":
                                worksheet.write(q, subfield.text)
                    if datafield.get("tag") == "952":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "6":
                                worksheet.write(r, subfield.text)
                    if datafield.get("tag") == "952":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "y":
                                worksheet.write(s, subfield.text)
                    if datafield.get("tag") == "942":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "n":
                                worksheet.write(t, subfield.text)
                    if datafield.get("tag") == "382":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a":
                                worksheet.write(u, subfield.text)
                    if datafield.get("tag") == "593":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            # print(subfield.tag, subfield.text)
                            if subfield.get("code") == "a":
                                worksheet.write(v, subfield.text)

                """traitement ajout du nouvel identifant en 773 et 774 si correspondant à l'ancien 001_RISM"""
                tag_773_w = []            
                tag_774_w = []
                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") =="773":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="w":
                                # print(subfield.text, records[subfield.text])
                                tag_773_w.append(subfield.text)
                worksheet.write(m, str(tag_773_w))
                for datafield in elt.findall("{http://www.loc.gov/MARC21/slim}datafield"):
                    if datafield.get("tag") =="774":
                        for subfield in datafield.findall("{http://www.loc.gov/MARC21/slim}subfield"):
                            if subfield.get("code") =="w":
                                # print(subfield.text, records[subfield.text])
                                tag_774_w.append(subfield.text)
                worksheet.write(n, str(tag_774_w))                              
                elt.clear()
        
        # csv_writer.writerows([doublons])
        # print(values_852)
        workbook.close()
        # csv_file.close()
        print("finished ! parsed count",count)
        """Securité"""
        if count > 60000:
            sys.exit("Too long script")        
    except FileNotFoundError:
        print("file not found")







if __name__ == "__main__":
    main()