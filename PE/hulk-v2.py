import sys
import io
import os
import json
from datetime import datetime
from ncclient import manager
import xml.dom.minidom
import xml.etree.ElementTree as ET

from tasks import *
from filters import *

# ✅ FIX UTF-8 (voorkomt GitHub runner errors)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# -----------------------------
# LOGGING SYSTEM
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

# -----------------------------
# PRETTY XML
# -----------------------------
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

# -----------------------------
# PAYLOAD VIEW
# -----------------------------
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

def show_yang_modules(task_name, payload):
    modules = extract_yang_modules(payload)

    print("\n📦 YANG Modules gebruikt:")
    for mod in modules:
        print(f"   - {mod}")

# -----------------------------
# RESPONSE INTERPRETATIE 🔥
# -----------------------------
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
        if root.find('.//nc:ok', ns) is not None:
            print("✅ SUCCESS (config toegepast)")

            log_to_file(f"[SUCCESS] {task_name} → config applied")
            add_json_log(task_name, "SUCCESS", "config applied")
            return

        # ✅ DATA (read)
        if root.find('.//nc:data', ns) is not None:
            print("✅ SUCCESS (data ontvangen)")

            log_to_file(f"[SUCCESS] {task_name} → data retrieved")
            add_json_log(task_name, "SUCCESS", "data retrieved")
            return

        print("⚠️ UNKNOWN RESPONSE")
        log_to_file(f"[UNKNOWN] {task_name}")
        add_json_log(task_name, "UNKNOWN", "unknown response")

    except Exception as e:
        print("❌ PARSE ERROR:", e)
        log_to_file(f"[PARSE ERROR] {task_name} → {e}")
        add_json_log(task_name, "PARSE_ERROR", str(e))

# -----------------------------
# TASK SELECTOR
# -----------------------------
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
# DEVICE SELECT
# -----------------------------
device = sys.argv[1] if len(sys.argv) > 1 else "vrouter"

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

PORT = 830

# -----------------------------
# MAIN
# -----------------------------
def main():

    tasks = sys.argv[2:] if len(sys.argv) > 2 else ["get_hostname"]

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

        target_ds = "candidate" if use_candidate else "running"

        for task in tasks:

            mode, data = select_task(task)

            if mode is None:
                continue

            print(f"\n🚀 Running task: {task}")

            # ✅ payload + YANG
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

            interpret_netconf_response(response, task)

    save_json()
    print(f"\n📁 Logs: {LOG_FILE}")
    print(f"📄 JSON: {JSON_FILE}")

# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    main()