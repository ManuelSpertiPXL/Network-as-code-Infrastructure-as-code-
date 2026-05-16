import sys
import os
from ncclient import manager
import xml.dom.minidom

from tasks import *
from filters import *

# -----------------------------
# DEVICE SELECTIE
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
# PRETTY PRINT XML
# -----------------------------
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

# -----------------------------
# PAYLOAD DEBUG FUNCTION 🔥
# -----------------------------
def show_payload(task_name, payload):
    print("\n" + "="*60)
    print(f"📦 PAYLOAD for task: {task_name}")
    print("="*60)

    try:
        print(pretty_xml(str(payload)))
    except Exception:
        print(payload)

    print("="*60 + "\n")

import xml.etree.ElementTree as ET

def interpret_netconf_response(response):
    print("\n🔍 INTERPRETATIE:")

    try:
        root = ET.fromstring(str(response))

        # Namespace handling
        ns = {'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0'}

        # ✅ 1. Check ERROR
        rpc_error = root.find('.//nc:rpc-error', ns)
        if rpc_error is not None:
            print("❌ RESULT: ERROR DETECTED")

            error_type = rpc_error.find('nc:error-type', ns)
            error_tag = rpc_error.find('nc:error-tag', ns)
            error_severity = rpc_error.find('nc:error-severity', ns)
            error_message = rpc_error.find('nc:error-message', ns)

            print(f"   Type     : {error_type.text if error_type is not None else 'N/A'}")
            print(f"   Tag      : {error_tag.text if error_tag is not None else 'N/A'}")
            print(f"   Severity : {error_severity.text if error_severity is not None else 'N/A'}")
            print(f"   Message  : {error_message.text if error_message is not None else 'N/A'}")

            # Extra interpretatie
            if error_tag is not None:
                if error_tag.text == "data-missing":
                    print("   💡 Betekenis: veld ontbreekt")
                elif error_tag.text == "invalid-value":
                    print("   💡 Betekenis: ongeldige waarde")
                elif error_tag.text == "operation-failed":
                    print("   💡 Betekenis: operatie mislukt")
                elif error_tag.text == "unknown-element":
                    print("   💡 Betekenis: verkeerde YANG node / typo")
                elif error_tag.text == "bad-element":
                    print("   💡 Betekenis: fout in XML structuur")

            return

        # ✅ 2. Check OK (writes)
        ok = root.find('.//nc:ok', ns)
        if ok is not None:
            print("✅ RESULT: SUCCESS (config toegepast)")
            return

        # ✅ 3. Check DATA (reads)
        data = root.find('.//nc:data', ns)
        if data is not None:
            print("✅ RESULT: SUCCESS (data ontvangen)")
            return

        # ⚠️ fallback
        print("⚠️ RESULT: Onbekende response structuur")

    except Exception as e:
        print("❌ FOUT bij parsing response:", e)

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

        # -----------------------------
        # CAPABILITY CHECK
        # -----------------------------
        use_candidate = any(":candidate" in cap for cap in m.server_capabilities)

        if use_candidate:
            print("🟢 Candidate datastore supported")
            target_ds = "candidate"
        else:
            print("🟡 Using running datastore")
            target_ds = "running"

        # -----------------------------
        # TASK LOOP
        # -----------------------------
        for task in tasks:

            mode, data = select_task(task)

            if mode is None:
                continue

            print(f"\n🚀 Running task: {task}")

            # ✅ NIEUW: toon payload VOOR uitvoering
            if data:
                show_payload(task, data)

            # -----------------------------
            # READ
            # -----------------------------
            if mode == "GET":
                response = m.get(filter=data)

                print("📥 RESPONSE:")
                print(pretty_xml(str(response)))
                interpret_netconf_response(response)

            elif mode == "GET_CONFIG":
                response = m.get_config(source="running")

                print("📥 RUNNING CONFIG:")
                print(pretty_xml(str(response)))
                interpret_netconf_response(response)

            # -----------------------------
            # WRITE
            # -----------------------------
            elif mode == "CONFIG":

                if use_candidate:
                    print("🔒 Locking candidate datastore")
                    m.lock(target="candidate")

                try:
                    print("📤 Sending configuration")

                    response = m.edit_config(
                        target=target_ds,
                        config=data
                    )

                    print("📥 RESPONSE:")
                    print(pretty_xml(str(response)))
                    interpret_netconf_response(response)

                    if use_candidate:
                        print("✅ Committing configuration")
                        m.commit()
                    else:
                        print("✅ Applied to running datastore")

                except Exception as e:
                    print("❌ Error:", e)

                    if use_candidate:
                        print("↩️ Rolling back changes")
                        m.discard_changes()

                finally:
                    if use_candidate:
                        print("🔓 Unlocking datastore")
                        m.unlock(target="candidate")

# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    main()