# NETCONF Hulk v2.0 - The Ultimate NETCONF Testing Framework
# Deze versie is volledig herschreven met een focus op:
# - Modulaire structuur (taken + filters in aparte files)
# - Verbeterde logging (logt nu ook naar JSON voor makkelijke analyse)
# - YANG module detectie (toont welke YANG modules in de payload zitten)
# - Uitgebreide response interpretatie (probeert RPC errors te ontleden en te verklaren)
# - Flexibele task selector (kies welke taken je wilt uitvoeren via command line args)
# - En natuurlijk... de Hulk is sterker dan ooit! 
# 💪

# LET OP: deze code is bedoeld als educatief voorbeeld en is niet geschikt voor productiegebruik zonder verdere aanpassingen en beveiligingsmaatregelen.
# Gebruik deze code als basis voor je eigen NETCONF scripts en pas deze aan naar jouw behoeften!
# Veel plezier met experimenteren en leren over NETCONF! 
# 🚀

# IMPORTS
# (zorg dat je ncclient geïnstalleerd hebt: pip install ncclient)
# (en ook lxml voor XML parsing: pip install lxml)
# (en vergeet niet de taken en filters te definiëren in tasks.py en filters.py)
# (deze code is niet volledig, je moet de functies in tasks.py en filters.py zelf invullen op basis van de voorbeelden die ik eerder gaf)
# (zorg ook dat je de juiste device credentials in de environment variables hebt staan, of pas de code aan om ze direct in te vullen)
# (deze code is bedoeld om lokaal te draaien, maar je kunt hem ook aanpassen om op een server of in een CI/CD pipeline te draaien)
# (de code bevat uitgebreide logging naar een logbestand en een JSON bestand, zodat je later makkelijk kunt analyseren wat er gebeurd is)
# (de code is ook bedoeld om makkelijk aan te passen en uit te breiden, dus voel je vrij om nieuwe taken toe te voegen, of extra functies voor response interpretatie, of wat je maar wilt!)

import sys
import io
import os
import json
from datetime import datetime
from ncclient import manager
import xml.dom.minidom
import xml.etree.ElementTree as ET
from tabulate import tabulate
from urllib.parse import parse_qs

# Importeer taken en filters uit aparte modules
# Zorg dat je deze modules zelf aanmaakt en de functies invult op basis van de voorbeelden die ik eerder gaf
# (deze code zal niet werken zonder deze modules, dus zorg dat je ze aanmaakt en de functies invult voordat je deze code runt)
# from scripts.tasks import set_hostname
from tasks import *
from filters import *

# ✅ FIX UTF-8 (voorkomt GitHub runner errors door de charmaps van Windows)
# (deze regel zorgt ervoor dat de standaard output van het script in UTF-8 wordt gezet, wat problemen voorkomt bij het printen van bepaalde tekens in de GitHub runner omgeving)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# -----------------------------
# LOGGING SYSTEM
# -----------------------------
# Deze sectie bevat functies voor het loggen van gebeurtenissen naar een logbestand en een JSON bestand.
# Het logbestand bevat een leesbare tekstuele weergave van de gebeurtenissen, terwijl het JSON bestand gestructureerde data bevat die later geanalyseerd kan worden.
# De functies log_to_file en add_json_log worden gebruikt om gebeurtenissen te loggen, en de functie save_json slaat het JSON bestand op wanneer het script klaar is.
LOG_FILE = f"logs/netconf_{datetime.now().date()}.log"
JSON_FILE = "logs/netconf_output.json"
# Zorg dat de logs directory bestaat
os.makedirs("logs", exist_ok=True)
# Log een bericht naar het logbestand met een timestamp
def log_to_file(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
# JSON log entry toevoegen aan de json_output lijst
json_output = []
# Deze functie voegt een log entry toe aan de json_output lijst, die later wordt opgeslagen in een JSON bestand. 
# Elke entry bevat een timestamp, de naam van de taak, de status (bijv. SUCCESS, ERROR) en details over wat er gebeurd is.
def add_json_log(task, status, details):
    json_output.append({
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "status": status,
        "details": details
    })
# Deze functie slaat de json_output lijst op in een JSON bestand.
def save_json():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4)

# -----------------------------
# PRETTY XML
# -----------------------------
# Deze functie neemt een XML string en maakt er een mooi geformatteerde versie van, met inspringing en nieuwe regels, zodat het makkelijker te lezen is wanneer het geprint wordt.
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")


def parse_capability(cap):
    result = {
        "type": "",
        "module": "",
        "revision": ""
    }

    # 🔹 NETCONF base capabilities
    if cap.startswith("urn:ietf:params:netconf"):
        parts = cap.split(":")
        result["type"] = "netconf"
        result["module"] = parts[-2]
        result["revision"] = parts[-1]

    # 🔹 YANG modules met query (?module=...)
    elif "?module=" in cap:
        try:
            base, query = cap.split("?", 1)
            params = parse_qs(query)

            result["type"] = base.split("/")[2] if "://" in base else "yang"
            result["module"] = params.get("module", ["-"])[0]
            result["revision"] = params.get("revision", ["-"])[0]
        except:
            result["module"] = cap

    # 🔹 fallback
    else:
        result["module"] = cap

    return result


# Get capabilities in a nice table format (optioneel, kan gebruikt worden om de capabilities van het apparaat te tonen in een overzichtelijke tabel


def get_capabilities_table(m):
    table = []

    for cap in m.server_capabilities:
        parsed = parse_capability(cap)

        table.append([
            parsed["type"],
            parsed["module"],
            parsed["revision"]
        ])

    return tabulate(
        table,
        headers=["Type", "Module", "Revision"],
        tablefmt="simple"
    )



# -----------------------------
# PAYLOAD VIEW
# -----------------------------
# Deze functie toont de XML payload die naar het apparaat gestuurd gaat worden, in een mooi geformatteerde versie.
# Het helpt om te zien wat er precies naar het apparaat gestuurd wordt, en welke YANG modules er in de payload zitten.
def show_payload(task_name, payload):
    print("\n" + "="*60)
    print(f"📦 PAYLOAD for task: {task_name}")
    print("="*60)

    try:
        print(pretty_xml(str(payload)))
    except Exception:
        print(payload)

    print("="*60)

# -----------------------------
# YANG MODULE DETECTOR 🔥
# -----------------------------
# Deze functie probeert te detecteren welke YANG modules er in de XML payload gebruikt worden, door te kijken naar de XML namespaces.
# Het is een eenvoudige heuristiek die kijkt naar de XML tags en hun namespaces, en probeert daaruit de namen van de YANG modules af te leiden.
def extract_yang_modules(xml_payload):
    modules = set()

    try:
        root = ET.fromstring(str(xml_payload))

        for elem in root.iter():
            if elem.tag.startswith("{"):
                namespace = elem.tag.split("}")[0].strip("{")

                if "cisco.com/ns/yang" in namespace:
                    modules.add(namespace.split("/")[-1])

                elif "urn:" in namespace:
                    modules.add(namespace.split(":")[-1])

    except Exception:
        return ["(parse error)"]

    return list(modules)
# Deze functie toont de gedetecteerde YANG modules die in de payload gebruikt worden, zodat je een idee hebt van welke YANG modellen er aan het werk zijn bij deze taak.
# Het is een handige manier om snel inzicht te krijgen in de gebruikte YANG modules zonder de hele payload te hoeven analyseren.
def show_yang_modules(task_name, payload):
    modules = extract_yang_modules(payload)

    print("\n📦 YANG Modules gebruikt:")
    for mod in modules:
        print(f"   - {mod}")

# -----------------------------
# RESPONSE INTERPRETATIE 🔥
# -----------------------------
# Deze functie probeert de NETCONF response te interpreteren, door te kijken naar de XML structuur van de response.
# Het kijkt of er een <ok> element in de response zit (wat betekent dat de config succesvol toegepast is), of dat er een <rpc-error> element in de response zit (wat betekent dat er een fout is opgetreden).
# Als er een fout is opgetreden, probeert het de details van de fout te extraheren, zoals het type fout, de tag, de severity en het foutbericht, en geeft het ook een korte uitleg van wat de fout betekent.
# Het logt ook de resultaten van de interpretatie naar het logbestand en het JSON bestand, zodat je later makkelijk kunt analyseren wat er gebeurd is en welke fouten er zijn opgetreden.
def interpret_netconf_response(response, task_name):
    print("\n🔍 INTERPRETATIE:")

    try:
        root = ET.fromstring(str(response))
        ns = {'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0'}

        # ❌ ERROR
        rpc_error = root.find('.//nc:rpc-error', ns)
        if rpc_error is not None:
            err = {
                "type": rpc_error.findtext('nc:error-type', default="N/A", namespaces=ns),
                "tag": rpc_error.findtext('nc:error-tag', default="N/A", namespaces=ns),
                "severity": rpc_error.findtext('nc:error-severity', default="N/A", namespaces=ns),
                "message": rpc_error.findtext('nc:error-message', default="N/A", namespaces=ns),
            }

            print("❌ ERROR DETECTED:")
            for k, v in err.items():
                print(f"   {k:<10}: {v}")

            # Extra betekenis
            # Hier kun je extra uitleg geven over wat de fout betekent, op basis van de error tag of type. 
            # Dit is natuurlijk niet uitputtend, maar het kan helpen om snel te begrijpen wat er mis is gegaan.
            explanations = {
                "invalid-value": "ongeldige waarde",
                "data-missing": "veld ontbreekt",
                "unknown-element": "verkeerde YANG node",
                "bad-element": "syntax/XML fout",
                "operation-failed": "operatie mislukt"
            }

            if err["tag"] in explanations:
                print(f"   💡 Betekenis: {explanations[err['tag']]}")

            log_to_file(f"[ERROR] {task_name} → {err}")
            add_json_log(task_name, "ERROR", err)
            return

        # ✅ OK (write)
        # Als er een <ok> element in de response zit, betekent dit dat de config succesvol is toegepast.
        if root.find('.//nc:ok', ns) is not None:
            print("✅ SUCCESS (config toegepast)")
            # Log de succesvolle configuratie naar het logbestand en het JSON bestand, zodat je later makkelijk kunt analyseren welke taken succesvol waren en welke niet.
            log_to_file(f"[SUCCESS] {task_name} → config applied")
            add_json_log(task_name, "SUCCESS", "config applied")
            return

        # ✅ DATA (read)
        # Als er een <data> element in de response zit, betekent dit dat er data is teruggekomen van het apparaat (bijvoorbeeld bij een get of get-config operatie).
        # Dit betekent dat de operatie succesvol was en er data is ontvangen, dus we loggen dit ook als een succes.
        if root.find('.//nc:data', ns) is not None:
            print("✅ SUCCESS (data ontvangen)")
            # Log de succesvolle data retrieval naar het logbestand en het JSON bestand, zodat je later makkelijk kunt analyseren welke taken succesvol waren en welke niet.
            log_to_file(f"[SUCCESS] {task_name} → data retrieved")
            add_json_log(task_name, "SUCCESS", "data retrieved")
            return
        # ⚠️ UNKNOWN RESPONSE
        # Als er geen <ok>, <rpc-error> of <data> element in de response zit, betekent dit dat we een onbekende response hebben ontvangen die we niet kunnen interpreteren.
        # We loggen dit als een waarschuwing, zodat je later kunt analyseren welke taken een onbekende response hebben opgeleverd, wat kan duiden op onverwachte fouten of situaties die niet goed worden afgehandeld door de interpretatiefunctie.
        print("⚠️ UNKNOWN RESPONSE")
        log_to_file(f"[UNKNOWN] {task_name}")
        add_json_log(task_name, "UNKNOWN", "unknown response")
    # Als er een fout optreedt tijdens het parsen van de response, loggen we dit als een parse error, zodat je later kunt analyseren welke taken problemen hebben met het parsen van de response, wat kan duiden op ernstige fouten in de communicatie of onverwachte response formats.
    except Exception as e:
        print("❌ PARSE ERROR:", e)
        log_to_file(f"[PARSE ERROR] {task_name} → {e}")
        add_json_log(task_name, "PARSE_ERROR", str(e))

# -----------------------------
# TASK SELECTOR
# -----------------------------
# Deze functie selecteert welke taak uitgevoerd moet worden op basis van de command line argumenten.
# Je kunt hier nieuwe taken toevoegen door een nieuwe elif tak toe te voegen die de naam van de taak vergelijkt en de bijbehorende mode (GET, GET_CONFIG, CONFIG) en data (XML payload of filter) teruggeeft.

# TAKEN die deel uitmaken van de 39 taken uit LAB 8.2
def select_task(task_name):
    # Basis taken
    if task_name == "task1":
        return "CONFIG", task1_interface_description()
    elif task_name == "task2":
        return "CONFIG", task2_interface_enable()
    elif task_name == "task3":
        return "CONFIG", task3_set_ipv4()
    elif task_name == "task4":
        return "CONFIG", task4_remove_ipv4()
    elif task_name == "task5":
        return "CONFIG", task5_create_loopback()
    elif task_name == "task6":
        return "CONFIG", task6_loopback_ip()
    elif task_name == "task7":
        return "CONFIG", task7_set_hostname()
    elif task_name == "task8":
        return "GET", task8_dns()
    elif task_name == "task9":
        return "GET_CONFIG", task9_ntp()
    elif task_name == "task10":
        return "CONFIG", task10_static_route()
    elif task_name == "task11":
        return "CONFIG", task11_no_static_route()
    elif task_name == "task12":
        return "CONFIG", task12_motd()
    elif task_name == "task13":
        return "CONFIG", task13_create_local_user()
    elif task_name == "task14":
        return "CONFIG", task14_mod_user_password()
    elif task_name == "task15":
        return "CONFIG", task15_create_vlan()
    elif task_name == "task16":
        return "CONFIG", task16_vlan_interface()
    elif task_name == "task17":
        return "CONFIG", task17_snmp()
    elif task_name == "task18":
        return "GET", task18_if_stats()
    elif task_name == "task19":
        return "GET", task19_running_config()
    elif task_name == "task20":
        return "CONFIG", task20_val_config()
    # geavanceerdere taken

    elif task_name == "task21":
        return "CONFIG", task21_ds_candidate_com_if()
    elif task_name == "task22":
        return "CONFIG", task22_ds_lock_ulock()
    elif task_name == "task23":
        return "CONFIG", task23_multi_if()
    elif task_name == "task24":
        return "CONFIG", task24_rollback()
    elif task_name == "task25":
        return "CONFIG", task25_diff_run_cand()
    elif task_name == "task26":
        return "CONFIG", task26_ipv6()
    elif task_name == "task27":
        return "CONFIG", task27_ospf()
    elif task_name == "task28":
        return "CONFIG", task28_routing()
    elif task_name == "task29":
        return "CONFIG", task29_MTU()
    elif task_name == "task30":
        return "CONFIG", task30_ACL()
    elif task_name == "task31":
        return "CONFIG", task31_speed_duplex()
    elif task_name == "task32":
        return "CONFIG", task32_yang_action()
    elif task_name == "task33":
        return "CAPABILITIES", None
    elif task_name == "task34":
        return "config", task34_openCONFIG()
    elif task_name == "task35":
        return "config", task35_full_deploy()
    else:
        print("ERROR: Unknown task")
        return None, None

"""     if task_name == "task7":
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
    elif task_name == "get_hostname_and_interfaces":
        return "GET", get_hostname_and_interfaces() """
"""     elif task_name == "get_hostname":
        return "GET", get_hostname_filter()
    elif task_name == "get_motd":
        return "GET", get_motd_filter()
    elif task_name == "set_hostname":
        return "CONFIG", set_hostname()
    elif task_name == "get_hostname_and_interfaces":
        return "GET", get_hostname_and_interfaces()
    elif task_name == "get_routing":
        return "GET", get_routing_filter()
    elif task_name == "get_interfaces":
        return "GET", get_interfaces_filter()
    elif task_name == "get_capabilities":
        return "CAPABILITIES", None """


# -----------------------------
# DEVICE SELECT
# -----------------------------
# Deze sectie selecteert welke device we gaan benaderen op basis van de command line argumenten.
# Je kunt hier nieuwe devices toevoegen door een nieuwe elif tak toe te voegen die de naam van het device vergelijkt en de bijbehorende IP, username en password teruggeeft (bijvoorbeeld uit environment variables).
device = sys.argv[1] if len(sys.argv) > 1 else "vrouter"
# Hier worden de credentials voor de verschillende devices opgehaald uit environment variables.
# Zorg ervoor dat je deze environment variables hebt ingesteld voordat je het script runt, of pas de code aan om de credentials direct in te vullen (let op: dit is niet veilig voor productiegebruik).
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
# Standaard NETCONF poort
PORT = 830

# -----------------------------
# MAIN
# -----------------------------
# Hier worden de taken gedefinieerd die kunnen worden uitgevoerd, met bijbehorende XML payloads of filters.
# Je kunt hier nieuwe taken toevoegen door een nieuwe functie te definiëren die de XML payload of filter teruggeeft, en deze functie vervolgens toe te voegen aan de select_task functie hierboven.

def main():
    # Hier worden de taken geselecteerd die uitgevoerd moeten worden op basis van de command line argumenten.
    # Je kunt meerdere taken tegelijk uitvoeren door meerdere taaknamen als command line argumenten mee te geven, bijvoorbeeld: python hulk.py task7 get_interfaces get_hostname
    # Als er geen taken zijn opgegeven, gebruiken we een standaard taak (in dit geval "get_hostname") zodat het script niet zonder actie eindigt.
    # Je kunt dit aanpassen naar een andere standaard taak, of het leeg laten als je wilt dat er geen actie wordt uitgevoerd zonder expliciete taakselectie.
    
# 🔥 CLI parsing (device + store_mode + tasks)
    store_mode = sys.argv[2] if len(sys.argv) > 2 else "auto"

    tasks = sys.argv[2:] if len(sys.argv) > 2 else ["get_hostname"]
    # Verbinden met het apparaat via NETCONF en uitvoeren van de geselecteerde taken
    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={"name": "iosxe"}
    ) as m:
        # ✅ Verbonden met toestel
        print(f"\n✅ Verbonden met toestel: {device} ({HOST})")
        # -----------------------------
        # CAPABILITY CHECK & CANDIDATE CHECK
        # -----------------------------
        # Hier controleren we de capabilities van het apparaat om te zien of het de "candidate" datastore ondersteunt, wat belangrijk is voor write operaties.
        # 🔥 detect candidate support
        use_candidate = any(":candidate" in cap for cap in m.server_capabilities)

        

        # 🔥 store selection
        if store_mode == "candidate":
            if not use_candidate:
                print("❌ Candidate niet supported")
                exit(1)
            target_ds = "candidate"

        elif store_mode == "running":
            target_ds = "running"

        else:
            target_ds = "candidate" if use_candidate else "running"

        print(f"📌 Store mode: {store_mode}")
        print(f"📌 Target datastore: {target_ds}")

        
        for task in tasks:
            # Hier selecteren we de mode (GET, GET_CONFIG, CONFIG) en de data (XML payload of filter) voor de huidige taak, door de select_task functie aan te roepen.
            mode, data = select_task(task)
            # Als de taak onbekend is (mode is None), slaan we deze taak over en gaan we door naar de volgende taak in de lijst.
            if mode is None:
                continue
            # Hier tonen we de payload die we gaan gebruiken voor deze taak, zodat we kunnen zien wat er precies naar het apparaat gestuurd gaat worden.
            print(f"\n🚀 Running task: {task}")

            
            # ✅ capabilities speciale case
            if mode == "CAPABILITIES":
                print("\n📡 DEVICE CAPABILITIES:\n")
                print(get_capabilities_table(m))
                continue


            # ✅ payload + YANG
            # We tonen de payload die we gaan gebruiken voor deze taak, en ook welke YANG modules er in de payload gebruikt worden, zodat we een beter inzicht hebben in wat er precies gebeurt bij deze taak.
            if data:
                show_payload(task, data)
                show_yang_modules(task, data)

            if mode == "GET":
                response = m.get(filter=data)

            elif mode == "GET_CONFIG":
                response = m.get_config(source="running")

            elif mode == "CONFIG":
                if use_candidate:
                    m.lock(target="candidate")

                try:
                    response = m.edit_config(
                        target=target_ds,
                        config=data
                    )
                    if use_candidate:
                        m.commit()
                finally:
                    if use_candidate:
                        m.unlock(target="candidate")

            print("\n📥 RESPONSE:")
            print(pretty_xml(str(response)))
            # Hier proberen we de response te interpreteren, om te zien of de operatie succesvol was, of dat er een fout is opgetreden, en wat de details van die fout zijn als dat het geval is.

            interpret_netconf_response(response, task)

    save_json()
    print(f"\n📁 Logs: {LOG_FILE}")
    print(f"📄 JSON: {JSON_FILE}")

# -----------------------------
# START
# -----------------------------
# Hier starten we het script door de main functie aan te roepen.
if __name__ == "__main__":
    main()