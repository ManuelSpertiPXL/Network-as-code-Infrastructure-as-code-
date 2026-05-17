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

# -----------------------------
# XML HELPERS
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
        try:
            base, query = cap.split("?", 1)
            params = parse_qs(query)

            result["type"] = base.split("/")[2] if "://" in base else "yang"
            result["module"] = params.get("module", ["-"])[0]
            result["revision"] = params.get("revision", ["-"])[0]
        except:
            result["module"] = cap

    else:
        result["module"] = cap

    return result


def get_capabilities_table(m):
    table = []

    for cap in m.server_capabilities:
        parsed = parse_capability(cap)
        table.append([
            parsed["type"],
            parsed["module"],
            parsed["revision"]
        ])

    return tabulate(table, headers=["Type", "Module", "Revision"], tablefmt="grid")

# -----------------------------
# PAYLOAD + YANG
# -----------------------------
def show_payload(task_name, payload):
    print("\n" + "="*60)
    print(f"📦 PAYLOAD for task: {task_name}")
    print("="*60)

    try:
        print(pretty_xml(str(payload)))
    except:
        print(payload)

    print("="*60)


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

    except:
        return ["(parse error)"]

    return list(modules)


def show_yang_modules(task_name, payload):
    modules = extract_yang_modules(payload)

    print("\n📦 YANG Modules gebruikt:")
    for mod in modules:
        print(f"   - {mod}")

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
                print(f"{k:<10}: {v}")

            add_json_log(task_name, "ERROR", err)
            return

        if root.find('.//nc:ok', ns) is not None:
            print("✅ SUCCESS (config toegepast)")
            add_json_log(task_name, "SUCCESS", "config applied")
            return

        if root.find('.//nc:data', ns) is not None:
            print("✅ SUCCESS (data ontvangen)")
            add_json_log(task_name, "SUCCESS", "data retrieved")
            return

        print("⚠️ UNKNOWN RESPONSE")

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
    elif task_name == "task7":
        return "CONFIG", task7_set_hostname()
    elif task_name == "task8":
        return "GET", task8_dns()
    elif task_name == "task9":
        return "GET_CONFIG", task9_ntp()
    elif task_name == "task33":
        return "CAPABILITIES", None
    elif task_name == "get_hostname":
        return "GET", get_hostname()
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

                    validate_change(m)

                finally:
                    if use_candidate:
                        m.unlock(target="candidate")

            elif mode == "CAPABILITIES":
                print("\n📊 CAPABILITIES:")
                print(get_capabilities_table(m))

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