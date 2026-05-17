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

from tasks import *
from filters import *

# UTF-8 fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# -----------------------------
# LOGGING
# -----------------------------
LOG_FILE = f"logs/netconf_{datetime.now().date()}.log"
JSON_FILE = "logs/netconf_output.json"

os.makedirs("logs", exist_ok=True)

def log_to_file(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

json_output = []

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
# XML HELPERS
# -----------------------------
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

# -----------------------------
# RESPONSE INTERPRET
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

# -----------------------------
# TASK SELECTOR
# -----------------------------
def select_task(task_name):
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
        return "CONFIG", task34_openCONFIG()
    elif task_name == "task35":
        return "CONFIG", task35_full_deploy()
    elif task_name == "get_hostname":
        return "GET", get_hostname()
    elif task_name == "get_capabilities":
        return "CAPABILITIES", None
    else:
        print(f"❌ Unknown task: {task_name}")
        return None, None

# -----------------------------
# DEVICE SELECT
# -----------------------------
device = sys.argv[1] if len(sys.argv) > 1 else "vrouter"

if device == "vrouter":
    HOST = os.getenv("VROUTER_IP")
    USER = os.getenv("VROUTER_USER")
    PASS = os.getenv("VROUTER_PASS")
else:
    print("❌ Unknown device")
    exit(1)

PORT = 830

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
    store_mode = sys.argv[2] if len(sys.argv) > 2 else "auto"
    tasks = sys.argv[3:] if len(sys.argv) > 3 else ["get_hostname"]

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

        # ✅ FIXED LOOP (binnen connectie!)
        for task in tasks:
            response = None

            mode, data = select_task(task)

            if mode is None:
                continue

            print(f"\n🚀 Running task: {task}")
            
            if data is not None:
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
                        m.validate(source='candidate')
                        m.commit()
                    else:
                        # IOS-XE → auto apply
                        pass

                    validate_change(m)

                finally:
                    if use_candidate:
                        m.unlock(target="candidate")

            elif mode == "CAPABILITIES":
                print("\n📊 CAPABILITIES:")
                for cap in m.server_capabilities:
                    print(cap)

            # RESPONSE handling
            if response is not None:
                print("\n📥 RESPONSE:")
                print(pretty_xml(str(response)))
                interpret_netconf_response(response, task)

    save_json()
    print(f"\n📁 Logs: {LOG_FILE}")
    print(f"📄 JSON: {JSON_FILE}")

# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    main()