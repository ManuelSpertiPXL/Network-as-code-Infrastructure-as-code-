# HULK version 2.4 - NETCONF TASK EXECUTOR

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
import difflib
from tasks import *
from filters import *
from ncclient.xml_ import to_ele
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# -----------------------------
# LOGGING
# -----------------------------
LOG_FILE = f"logs/netconf_{datetime.now().date()}.log"
JSON_FILE = "logs/netconf_output.json"
os.makedirs("logs", exist_ok=True)

json_output = []

def log_to_file(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def add_json_log(task, status, details):
    json_output.append({
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "status": status,
        "details": details
    })

def save_json():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4)

# -----------------------------
# XML
# -----------------------------
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

# -----------------------------
# CAPABILITIES
# -----------------------------
def parse_capability(cap):
    result = {"type": "", "module": "", "revision": ""}

    if cap.startswith("urn:ietf:params:netconf"):
        parts = cap.split(":")
        result["type"] = "netconf"
        result["module"] = parts[-2]
        result["revision"] = parts[-1]

    elif "?module=" in cap:
        base, query = cap.split("?", 1)
        params = parse_qs(query)
        result["type"] = base.split("/")[2] if "://" in base else "yang"
        result["module"] = params.get("module", ["-"])[0]
        result["revision"] = params.get("revision", ["-"])[0]

    else:
        result["module"] = cap

    return result


def get_capabilities_table(m):
    table = []
    for cap in m.server_capabilities:
        p = parse_capability(cap)
        table.append([p["type"], p["module"], p["revision"]])
    return tabulate(table, headers=["Type", "Module", "Revision"], tablefmt="grid")

# -----------------------------
# PAYLOAD + YANG
# -----------------------------
def show_payload(task_name, payload):
    print("\n" + "="*60)
    print(f"📦 PAYLOAD for task: {task_name}")
    print("="*60)
    print(pretty_xml(str(payload)))
    print("="*60)

def extract_yang_modules(xml_payload):
    modules = set()
    root = ET.fromstring(str(xml_payload))
    for elem in root.iter():
        if elem.tag.startswith("{"):
            ns = elem.tag.split("}")[0].strip("{")
            if "cisco.com/ns/yang" in ns:
                modules.add(ns.split("/")[-1])
            elif "urn:" in ns:
                modules.add(ns.split(":")[-1])
    return list(modules)

def show_yang_modules(task_name, payload):
    print("\n📦 YANG modules:")
    for m in extract_yang_modules(payload):
        print(f" - {m}")

# -----------------------------
# RESPONSE
# -----------------------------
def interpret_netconf_response(response, task_name):
    print("\n🔍 INTERPRETATIE:")

    try:
        root = ET.fromstring(str(response))
        ns = {'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0'}

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

            log_to_file(f"[ERROR] {task_name} → {err}")
            add_json_log(task_name, "ERROR", err)
            return

        if root.find('.//nc:ok', ns) is not None:
            print("✅ SUCCESS (config toegepast)")
            log_to_file(f"[SUCCESS] {task_name}")
            add_json_log(task_name, "SUCCESS", "config applied")
            return

        if root.find('.//nc:data', ns) is not None:
            print("✅ SUCCESS (data ontvangen)")
            log_to_file(f"[SUCCESS] {task_name}")
            add_json_log(task_name, "SUCCESS", "data retrieved")
            return

        print("⚠️ UNKNOWN RESPONSE")
        add_json_log(task_name, "UNKNOWN", "unknown response")

    except Exception as e:
        print("❌ PARSE ERROR:", e)
        add_json_log(task_name, "PARSE_ERROR", str(e))


def fetch_from_github():
    url = "https://raw.githubusercontent.com/ManuelSpertiPXL/Network-as-code-Infrastructure-as-code-/refs/heads/main/PE/36_end_to_end_config.xml"
    r = requests.get(url)
    
    if r.status_code != 200:
            print(f"❌ GitHub error: {r.status_code}")
            return None

    return r.text

# -----------------------------
# TASK SELECTOR (NIETS VERWIJDERD)
# -----------------------------
def select_task(task_name):
    if task_name == "task1": return "CONFIG", task1_interface_description()
    elif task_name == "task2": return "CONFIG", task2_interface_enable()
    elif task_name == "task3": return "CONFIG", task3_set_ipv4()
    elif task_name == "task4": return "CONFIG", task4_remove_ipv4()
    elif task_name == "task5": return "CONFIG", task5_create_loopback()
    elif task_name == "task6": return "CONFIG", task6_loopback_ip()
    elif task_name == "task7": return "CONFIG", task7_set_hostname()
    elif task_name == "task8": return "CONFIG", task8_dns()
    elif task_name == "task9": return "CONFIG", task9_ntp()
    elif task_name == "task10": return "CONFIG", task10_static_route()
    elif task_name == "task11": return "CONFIG", task11_no_static_route()
    elif task_name == "task12": return "CONFIG", task12_motd()
    elif task_name == "task13": return "CONFIG", task13_create_local_user()
    elif task_name == "task14": return "CONFIG", task14_mod_user_password()
    elif task_name == "task15": return "CONFIG", task15_create_vlan()
    elif task_name == "task16": return "CONFIG", task16_vlan_interface()
    elif task_name == "task17": return "CONFIG", task17_snmp()
    elif task_name == "task18": return "GET", task18_if_stats()
    elif task_name == "task19": return "GET", task19_running_config()
    elif task_name == "task20": return "CONFIG", task20_val_config()
    elif task_name == "task21": return "CONFIG", task21_ds_candidate_com_if(),True # True = candidate supported, dus lock/unlock gebruiken
    elif task_name == "task22": return "CONFIG", task22_ds_lock_unlock(), True  # True = candidate supported, dus lock/unlock gebruiken
    elif task_name == "task23": return "CONFIG", task23_multi_if()
    elif task_name == "task24": return "ROLLBACK", None # gebeurt automatisch bij error. 
    elif task_name == "task25": return "COMPARE", None # gebeurt automatisch bij candidate store.
    elif task_name == "task26": return "CONFIG", task26_ipv6() 
    elif task_name == "task27": return "CONFIG", task27_ospf()
    elif task_name == "task28": return "GET", task28_routing()
    elif task_name == "task29": return "CONFIG", task29_MTU()
    elif task_name == "task30": return "CONFIG", task30_acl()
    elif task_name == "task31": return "CONFIG", task31_speed_duplex()
    elif task_name == "task32": return "ACTION", None
    elif task_name == "task33": return "CAPABILITIES", None 
    elif task_name == "task34": return "CONFIG", task34_openCONFIG()
    elif task_name == "task35": return "CONFIG", task35_full_deploy()
    elif task_name == "task36": return "CONFIG", task36_end_to_end()
    elif task_name == "fetch_github": return "CONFIG", fetch_from_github()
    elif task_name == "get_hostname": return "GET", get_hostname()
    elif task_name == "get_capabilities": return "CAPABILITIES", None
    else:
        print("❌ Unknown task")
        return None, None

# -----------------------------
# DEVICE
# -----------------------------
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
# VALIDATE
# -----------------------------
def validate_change(m, filter_xml=None):
    print("\n🔎 VALIDATING CONFIG...")
    config = m.get_config(source="running", filter=filter_xml)
    print(pretty_xml(str(config)))

# -----------------------------
# MAIN
# -----------------------------
def main():
    store_mode = sys.argv[2] if len(sys.argv) > 1 else "auto"
    tasks = sys.argv[3:] if len(sys.argv) > 2 else ["task36"]
    backup_config = None
    print(f"DEBUG tasks: {tasks}")

    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={"name": "iosxe"}
    ) as m:

        print(f"\n✅ Verbonden met toestel: {device} ({HOST})")

        use_candidate = any(":candidate" in cap for cap in m.server_capabilities)

        if store_mode == "candidate":
            if not use_candidate:
                print("❌ Candidate niet supported")
                return
            target_ds = "candidate"
        elif store_mode == "running":
            target_ds = "running"
        else:
            target_ds = "candidate" if use_candidate else "running"

        print(f"📌 Store mode: {store_mode}")
        print(f"📌 Target datastore: {target_ds}")

        for task in tasks:
            response = None

            result = select_task(task)

            if result is None:
                continue

            if len(result) == 3:
                mode, data, requires_candidate = result
            else:
                mode, data = result
                requires_candidate = False
            
            if requires_candidate and not use_candidate:
                print(f"❌ Task {task} vereist candidate datastore")
                continue

            if mode is None:
                continue

            print(f"\n🚀 Running task: {task}")

            if data and data.strip().startswith("<"):
                show_payload(task, data)
                show_yang_modules(task, data)
            else:
                print("⚠️ GitHub gaf geen geldige XML terug")
                
                if data:
                    print(data[:200])


            if mode == "GET":
                response = m.get(filter=data)

            elif mode == "GET_CONFIG":
                response = m.get_config(source="running")

            elif mode == "CONFIG":
                backup_config = m.get_config(source="running")
                print("💾 Backup of running config stored")

                if use_candidate:
                    m.lock(target="candidate")
                    print("🔒 Candidate locked")

                try:
                    response = m.edit_config(
                        target=target_ds,
                        config=data
                    )

                    if use_candidate:
                        m.validate(source='candidate')
                        print("✅ Candidate validated, committing...")
                        m.commit()
                        print("✅ Candidate committed")

                    validate_change(m)
                    print("✅ Config change validated")

                finally:
                    if use_candidate:
                        m.unlock(target="candidate")
                        print("🔓 Candidate unlocked")

            elif mode == "CAPABILITIES":
                print("\n📊 CAPABILITIES:")
                for cap in m.server_capabilities:
                    print(cap)

            elif mode == "ROLLBACK":
                if backup_config is None:
                    print("❌ No backup available")
                    continue

                print("↩️ Rolling back config...")

                if use_candidate:
                    m.lock(target="candidate")
                    print("🔒 Candidate locked")

                try:
                    m.edit_config(target="candidate", config=backup_config)
                    m.commit()
                    print("✅ Rollback committed")

                finally:
                    if use_candidate:
                        m.unlock(target="candidate")
                        print("🔓 Candidate unlocked")


            # ✅ HIER KOMT COMPARE
            elif mode == "COMPARE":
                if not use_candidate:
                    print("❌ Candidate datastore nodig voor vergelijking")
                    continue

                print("🔍 Comparing running vs candidate configuration...")

                running = m.get_config(source="running")
                candidate = m.get_config(source="candidate")

                diff = difflib.unified_diff(
                    str(running).splitlines(),
                    str(candidate).splitlines(),
                    fromfile="running",
                    tofile="candidate",
                    lineterm=""
                )

                print("\n🔎 CONFIG DIFFERENCES:")
                found_diff = False

                for line in diff:
                    print(line)
                    found_diff = True

                if not found_diff:
                    print("✅ No differences found (configs are identical)")
                
            elif mode == "ACTION":
                print("🧹 Clearing interface counters...")

                rpc = task32_yang_actions()

                response = m.dispatch(to_ele(rpc))

            # RESPONSE handling
            if response is not None:
                print("\n📥 RESPONSE:")
                print(pretty_xml(str(response)))
                interpret_netconf_response(response, task)



    save_json()
    print(f"\n📁 Logs: {LOG_FILE}")
    print(f"📄 JSON: {JSON_FILE}")

# -----------------------------
if __name__ == "__main__":
    main()
