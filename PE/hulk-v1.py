# Deze code is een uitgebreid script dat verbinding maakt met een netwerkapparaat via NETCONF en verschillende taken kan uitvoeren op basis van de opgegeven argumenten. 
# Het script ondersteunt zowel lees- als schrijfoperaties, afhankelijk van de geselecteerde taak. 
# De code maakt gebruik van de ncclient-bibliotheek om de NETCONF-verbinding te beheren en XML-payloads te verzenden. 
# Er is ook een functie voor het mooi afdrukken van XML-responses. 
# De taken en filters worden geïmporteerd vanuit aparte modules, waardoor het script modulair en uitbreidbaar is.
import sys
import os
from ncclient import manager
import xml.dom.minidom
# Importeer taken en filters vanuit aparte modules. 
# Deze modules bevatten de XML-payloads en filters die worden gebruikt voor de verschillende taken die het script kan uitvoeren.
from tasks import *
from filters import *

# Gegevens voor verbinding met het netwerkapparaat. 
# In een echte omgeving zouden deze waarschijnlijk uit een configuratiebestand of omgevingsvariabelen komen.
# hardcoded values (for testing) voor noodzaak, maar in een echte omgeving zouden deze waarschijnlijk uit een configuratiebestand of omgevingsvariabelen komen.
# VROUTER
""" HOST = "192.168.56.105"
PORT = 830
USER = "cisco"
PASS = "cisco123!" """
# LAB ROUTER
""" HOST = "172.17.3.1"
PORT = 830
USER = "manuel"
PASS = "student@pxl!" """
# LAB SWITCH
""" HOST = "172.17.3.4"
PORT = 830
USER = "manuel"
PASS = "student@pxl!" """
# In plaats van hardcoded waarden te gebruiken, worden de verbindingsgegevens nu opgehaald uit omgevingsvariabelen.
# Dit maakt het script flexibeler en veiliger, omdat gevoelige informatie zoals wachtwoorden niet in de code zelf hoeft te worden opgeslagen.
device = sys.argv[1] if len(sys.argv) > 1 else "vrouter"
# Op basis van het opgegeven apparaat worden de juiste verbindingsgegevens opgehaald uit de omgevingsvariabelen.
# Er is ook een optie om verbinding te maken met een labrouter of labswitch, waarbij de verbindingsgegevens ook uit omgevingsvariabelen worden gehaald.
if device == "vrouter":
    HOST = os.getenv("VROUTER_IP")
    USER = os.getenv("VROUTER_USER")
    PASS = os.getenv("VROUTER_PASS")

elif device == "labrouter":
    HOST = os.getenv("LAB_ROUTER_IP")
    USER = os.getenv("LAB_ROUTER_USER")
    PASS = os.getenv("LAB_ROUTER_PASS")

elif device == "labswitch":
    HOST = os.getenv("LAB_SWITCH_IP")
    USER = os.getenv("LAB_SWITCH_USER")
    PASS = os.getenv("LAB_SWITCH_PASS")

else:
    print("ERROR: unknown device")
    exit(1)

PORT = 830 # Standaard NETCONF-poort

# -----------------------------
# PRETTY PRINT
# -----------------------------
# pretty_xml functie neemt een XML-string en retourneert een mooi geformatteerde versie van die string. 
# Dit maakt het gemakkelijker om de XML-responses van het netwerkapparaat te lezen en te begrijpen.
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

# -----------------------------
# TASK SELECTOR
# -----------------------------
# De select_task functie neemt een taaknaam als argument en retourneert het type operatie (GET, GET_CONFIG, CONFIG) en de bijbehorende XML-payload of filter. 
# Op basis van de taaknaam wordt de juiste functie aangeroepen die de XML-payload of filter retourneert.
def select_task(task_name):

    if task_name == "task7":
        return "CONFIG", task7_hostname()

    elif task_name == "task1":
        return "CONFIG", task1_interface_description()

    elif task_name == "task10":
        return "CONFIG", task10_static_route()

    elif task_name == "get_interfaces":
        return "GET", get_interfaces_filter()

    elif task_name == "get_running":
        return "GET_CONFIG", None

    elif task_name == "get_hostname":
        return "GET", get_hostname_filter()
    
    elif task_name == "get_motd":
        return "GET", get_motd_filter()
    
    elif task_name == "set_hostname":
        return "CONFIG", set_hostname()

    else:
        print("ERROR: Unknown task")
        return None, None


# -----------------------------
# MAIN
# -----------------------------
# De main functie is het startpunt van het script. 
# Het accepteert optioneel een lijst van taken als argumenten.
# Als er geen taken worden opgegeven, worden standaard de "get_hostname" en "get_motd" taken uitgevoerd.
# De functie maakt verbinding met het netwerkapparaat en voert de geselecteerde taken uit, waarbij de resultaten worden geprint in een mooi geformatteerde XML-indeling.
# Voor schrijfoperaties wordt ook gecontroleerd of de "candidate" datastore wordt ondersteund, en worden de wijzigingen correct beheerd met lock, commit en discard indien nodig.
# Na het uitvoeren van de taken wordt de verbinding met het netwerkapparaat gesloten.
def main():
    # Haal de lijst van taken op uit de commandoregelargumenten, of gebruik standaardtaken als er geen argumenten zijn opgegeven.
    tasks = sys.argv[1:] if len(sys.argv) > 1 else ["get_hostname", "get_motd"]
    # Maak verbinding met het netwerkapparaat met behulp van de ncclient manager.
    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={"name": "iosxe"}
    ) as m:

        print("Verbonden met toestel:",device, HOST)

        # -----------------------------
        # CAPABILITY CHECK (voor WRITE)
        # -----------------------------
        # Controleer of de "candidate" datastore wordt ondersteund door het netwerkapparaat. 
        # Als dit het geval is, worden configuratiewijzigingen eerst naar de "candidate" datastore gestuurd en vervolgens gecommit. 
        # Als de "candidate" datastore niet wordt ondersteund, worden wijzigingen direct naar de "running" datastore gestuurd.
        use_candidate = any(":candidate" in cap for cap in m.server_capabilities)

        if use_candidate:
            print("Candidate datastore supported")
            target_ds = "candidate"
        else:
            print("Using running datastore")
            target_ds = "running"

        # -----------------------------
        # TASK LOOP
        # -----------------------------
        # Loop door de geselecteerde taken en voer de bijbehorende operaties uit.
        # Voor elke taak wordt het type operatie en de bijbehorende XML-payload of filter opgehaald met de select_task functie.
        for task in tasks:

            mode, data = select_task(task)

            if mode is None:
                continue

            # -----------------------------
            # READ
            # -----------------------------
            # Voor leesoperaties (GET en GET_CONFIG) wordt de juiste NETCONF-operatie uitgevoerd met de opgegeven filter of payload, en wordt de response geprint in een mooi geformatteerde XML-indeling.
            # Voor GET_CONFIG wordt de configuratie opgehaald van de "running" datastore, terwijl voor GET een specifieke filter wordt gebruikt om alleen relevante informatie op te vragen.
            if mode == "GET":
                print(f"\nRunning task: {task}")
                response = m.get(filter=data)
                print(pretty_xml(str(response)))

            elif mode == "GET_CONFIG":
                print(f"\nRunning task: {task}")
                response = m.get_config(source="running")
                print(pretty_xml(str(response)))

            # -----------------------------
            # WRITE
            # ------------------------------
            # Voor schrijfoperaties (CONFIG) wordt de edit-config operatie gebruikt om de opgegeven XML-payload naar het netwerkapparaat te sturen.
            # Als de "candidate" datastore wordt gebruikt, worden de wijzigingen eerst naar de "candidate" datastore gestuurd en vervolgens gecommit.
            # Er is ook foutafhandeling aanwezig, waarbij eventuele fouten worden opgevangen en de wijzigingen worden teruggedraaid als er een fout optreedt tijdens het configureren.
            elif mode == "CONFIG":
                # Voor schrijfoperaties wordt eerst gecontroleerd of de "candidate" datastore wordt gebruikt. Als dit het geval is, wordt de datastore vergrendeld voordat de configuratie wordt verzonden.
                if use_candidate:
                    print("Locking candidate datastore")
                    m.lock(target="candidate")
                # Daarna wordt de configuratie verzonden met de edit-config operatie. Als er een fout optreedt tijdens het configureren, wordt deze opgevangen en worden eventuele wijzigingen teruggedraaid als de "candidate" datastore wordt gebruikt. Na het configureren wordt de datastore ontgrendeld als deze was vergrendeld.
                try:
                    print("Sending configuration")

                    response = m.edit_config(
                        target=target_ds,
                        config=data
                    )

                    print(pretty_xml(str(response)))
                    # Na het succesvol toepassen van de configuratie wordt er een commit uitgevoerd als de "candidate" datastore wordt gebruikt. Als de "candidate" datastore niet wordt gebruikt, is de configuratie al toegepast op de "running" datastore.
                    # Het committen van de configuratie zorgt ervoor dat de wijzigingen permanent worden gemaakt in de "running" datastore. Als er geen commit wordt uitgevoerd, blijven de wijzigingen in de "candidate" datastore en worden ze niet toegepast op de "running" datastore.
                    if use_candidate:
                        print("Committing configuration")
                        m.commit()
                    else:
                        print("Configuration applied to running")

                except Exception as e:
                    print("Error:", e)
                    # Als er een fout optreedt tijdens het configureren, worden eventuele wijzigingen teruggedraaid als de "candidate" datastore wordt gebruikt. Dit zorgt ervoor dat de configuratie in een consistente staat blijft, zelfs als er fouten optreden.
                    # Het terugdraaien van wijzigingen is alleen van toepassing als de "candidate" datastore wordt gebruikt, omdat in dat geval de wijzigingen nog niet zijn gecommit naar de "running" datastore. 
                    # Als er geen "candidate" datastore wordt gebruikt, worden wijzigingen direct toegepast op de "running" datastore en kunnen ze niet worden teruggedraaid.
                    if use_candidate:
                        m.discard_changes()
                # Na het configureren van de wijzigingen wordt de datastore ontgrendeld als deze was vergrendeld. Dit zorgt ervoor dat andere processen of gebruikers weer toegang hebben tot de datastore.
                # Het ontgrendelen van de datastore is belangrijk om te voorkomen dat deze per ongeluk vergrendeld blijft, wat problemen kan veroorzaken voor andere gebruikers of processen die toegang nodig hebben tot de datastore.
                finally:
                    if use_candidate:
                        print("Unlocking datastore")
                        m.unlock(target="candidate")

# -----------------------------
# START
# -----------------------------
# Het script wordt gestart door de main functie aan te roepen wanneer het script direct wordt uitgevoerd.
if __name__ == "__main__":
    main()