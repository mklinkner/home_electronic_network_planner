from pylatex import Document, Section, LongTable, NoEscape, Package, Tabularx, Hyperref
from pylatex.utils import bold
import os
import shutil

class Component:
    def __init__(self, name, cost, url):
        self.name = name
        self.cost = cost
        self.url = url

    def __str__(self):
        return f"{self.name}: {self.cost:.2f}€"

class Room:
    def __init__(self, name, components):
        self.name = name
        self.components = components  # List of tuples (Component, quantity)

    def __str__(self):
        return f"{self.name}:\n" + "\n".join([f"  {component} x {quantity}" for component, quantity in self.components])


def create_pdf(room, filename):
    # Create output directory if it doesn't exist
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Create LaTeX document with geometry package for margins
    doc = Document(documentclass='article', document_options='a4paper')
    doc.packages.append(Package('geometry', options='left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm'))
    doc.packages.append(Package('tabularx'))
    doc.packages.append(Package('longtable'))
    doc.packages.append(Package('hyperref'))

    with doc.create(Section(f"Raum: {str(room.name)}")):
        with doc.create(LongTable(">{\\raggedright\\arraybackslash}p{10cm} >{\\raggedleft\\arraybackslash}p{1.5cm} >{\\raggedleft\\arraybackslash}p{1.5cm} >{\\raggedleft\\arraybackslash}p{1.5cm}")) as table:
            table.add_hline()
            table.add_row([bold("Bauteil"), bold("Anzahl"), bold("Preis"), bold("Summe")])
            table.add_hline()
            table.end_table_header()
            # Sort components alphabetically by name
            sorted_components = sorted(room.components, key=lambda x: x[0].name)
            
            for component, quantity in sorted_components:
                if quantity > 0:
                    total_price = component.cost * quantity
                    component_name_with_link = NoEscape(f"\\href{{{component.url}}}{{{component.name}}}")
                    table.add_row([component_name_with_link, str(quantity), f"{component.cost:.2f}€", f"{total_price:.2f}€"])
            table.add_hline()
            table.add_row(["", "", bold("Summe:"), bold(f"{sum([component.cost * quantity for component, quantity in room.components if quantity > 0]):.2f}€")])

    # Save PDF and .tex files in the output directory
    doc.generate_pdf(os.path.join(output_dir, filename), clean_tex=False)
    # doc.generate_tex(os.path.join(output_dir, filename))


def main():
    # Define components
    single_switch = Component("Wippschalter-Einsatz Aus/Wechsel 2000/6", 5.44, "https://www.elektroland24.de/schalter-steckdosen/busch-jaeger/unterputzgeraete/schalter-taster/busch-jaeger-2000-6-us-wippschalter-einsatz-aus-wechsel.html")
    shutter_switch = Component("Jalousietaster-Einsatz 1-polig 2020/4", 23.81, "https://www.elektroland24.de/schalter-steckdosen/busch-jaeger/rollladensteuerung/schalter-taster-drehgriff/busch-jaeger-2020-4-us-jalousietaster-einsatz-1-polig.html")
    simple_socket = Component("Schutzkontakt-Steckdose 20EUC-84", 4.80, "https://www.elektroland24.de/schalter-steckdosen/busch-jaeger/suche-nach-material-farbe/alusilber-chrom/future-linear-alusilber/busch-jaeger-20euc-83-schutzkontakt-steckdose.html")
    enhanced_protection_socket = Component("Schutzkontakt-Steckdose mit erhöhtem Berührungsschutz 20EUCKS-84", 6.10, "https://www.elektroland24.de/schalter-steckdosen/busch-jaeger/suche-nach-material-farbe/gelb/axcent-gelb-studioweiss/busch-jaeger-20eucks-84-schutzkontakt-steckdose-mit-erhoehtem-beruehrungsschutz.html")
    shelly = Component("Shelly Plus 1", 13.99, "https://www.amazon.de/Shelly-elektronischen-kostenloser-Funktioniert-Garagentore/dp/B0965JN63Q/ref=sr_1_12?crid=J3EOBUU9JLJP&dib=eyJ2IjoiMSJ9.EN9Uz4XBnsRgnT4O-loS8Tjmc9gyT_ollRcC_tknqkPF59sAI_izEaRZiggfg7sPZfeJDoCrVNlJXhAfUqmNbyyU_rcYuqVvCqy_-9upiwemx7RrREu_32uVR4M4F4Ycib034cOolYTATFrG1uAdYwbXzaQ9F9AJTqAptrVUAauGGpTD2UlL_kf-dBYB9_wUQnCy-DW8tQS4mQUxljJ0tWUFLDRjGh-r4LNFw_T5jOrCfeR8seWj12X88ZGIrW7UOgrosJZnsQGu8JL26np64zvzqd0a2twBHCoHYKcBgJypEyvXINaqRKeF_Cm_B8wzgW2wKbKPTrb9zblbhTcbfv9RpFNzpzWllMB3XfkT03Dbn2av41ZHpTy8HIARvIWY5CJYpDQYc7fWcBc7ojAqKhOVAEo5u498TYLCxzZsC71A5eF69mfjZlesFD8VcV0g.Miy5Zqs6cdwjVjzHYbtiz3j7bY1qXcDrQVmtD4z8zDc&dib_tag=se&keywords=shelly%2Bunterputz%2Bsteckdose&qid=1739113332&sprefix=shelly%2Bunter%2Caps%2C129&sr=8-12&th=1")
    duplex_network_socket = Component("UAE-Anschlussdose 0218/12-101 2x RJ45 Cat.6A", 36.49, "https://www.elektroland24.de/schalter-steckdosen/busch-jaeger/unterputzgeraete/netzwerkdosen/busch-jaeger-0218-12-101-uae-anschlussdose-rj-45-cat.-6a-iso-2-fach.html")
    smoke_alarm = Component("Busch-Rauchalarm® ProfessionalLINE 6833-84 ", 23.94, "https://www.elektroland24.de/haustechnik/sicherheitstechnik/rauchmelder/busch-jaeger-6833-84-busch-rauchalarm-professionalline.html")
    # Define room with components and their quantities
    office = Room(
        "Büro", 
        [
            (single_switch, 2),
            (shutter_switch, 1),
            (simple_socket, 15),
            (shelly, 1),
            (enhanced_protection_socket, 0),
            (duplex_network_socket, 3),
            (smoke_alarm, 1),
        ]
    )

    # Print room information to PDF and .tex file
    create_pdf(office, "office_room")


if __name__ == "__main__":
    main()