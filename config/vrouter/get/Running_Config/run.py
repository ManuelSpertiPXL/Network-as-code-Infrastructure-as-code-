from ncclient import manager
import os
import pprint
# Deze code is gebaseerd op de code in config/router/set/hostname.py, maar in plaats van een edit-config operatie uit te voeren, wordt er een get-config operatie uitgevoerd. De payload is aangepast om een filter te bevatten dat alleen de hostname opvraagt. De response wordt vervolgens geprint, waarbij verschillende manieren worden getoond om de response te bekijken. De laatste print geeft een samenvatting van de response weer, inclusief eventuele foutmeldingen.
def load_xml():
    base = os.path.dirname(__file__)
    path = os.path.join(base, "run.xml")

    with open(path, "r") as f:
        return f.read()
# De push_config functie maakt verbinding met de netwerkapparaat en voert een get-config operatie uit met de payload als filter. De response wordt vervolgens geprint, waarbij verschillende manieren worden getoond om de response te bekijken. De laatste print geeft een samenvatting van de response weer, inclusief eventuele foutmeldingen.
def push_config():
    payload = load_xml()

    print("=== PAYLOAD ===")
    print(payload)
    print("===============")

    with manager.connect(
        host="192.168.56.105",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False,
        device_params={"name": "iosxe"}
    ) as m:

        print("Connected")

        response = m.get_config(
            source="running"
        )
        # Geeft aan dat de configuratie is opgehaald, maar geeft niet de configuratie zelf weer
        print("DONE")
        # Hieronder staan verschillende manieren om de response te bekijken. De eerste twee geven de configuratie weer, maar in een moeilijk leesbaar formaat. De laatste geeft een samenvatting van de response weer, inclusief eventuele foutmeldingen.
        print("==== RESPONSE ====")
        """ print(response.data_xml)
        print(response.xml) """
        # print(response) geeft een samenvatting van de response weer, inclusief eventuele foutmeldingen. Het is een handige manier om snel te zien of de configuratie succesvol is opgehaald, zonder dat je door een grote hoeveelheid XML hoeft te scrollen.
        """ print(response) """
        pprint.pprint(response)
        print("==================")
       

if __name__ == "__main__":
    push_config()
