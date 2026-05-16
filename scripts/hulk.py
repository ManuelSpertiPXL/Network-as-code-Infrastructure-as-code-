from ncclient import manager
import xml.dom.minidom
import xml.etree.ElementTree as ET
import sys
from tasks import *
from filters import *


HOST = "192.168.56.105"
PORT = 830
USER = "cisco"
PASS = "cisco123!"


# -----------------------------
# PRETTY PRINT XML
# -----------------------------
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")


# -----------------------------
# PARSE NETCONF RESPONSE
# -----------------------------
def parse_reply(xml):
    root = ET.fromstring(xml)

    if root.find(".//{*}ok") is not None:
        return " OK"

    errors = root.findall(".//{*}rpc-error")
    if errors:
        msgs = []
        for e in errors:
            msgs.append(e.findtext(".//{*}error-message"))
        return f" ERROR: {msgs}"

    return " Unknown response"


# -----------------------------
# XML PAYLOAD (EMBEDDED)
# -----------------------------
def get_payload():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <route>
            <ip-route-interface-forwarding-list>
              <prefix>10.10.99.0</prefix>
              <mask>255.255.255.0</mask>
              <fwd-list>
                <fwd>192.168.1.1</fwd>
              </fwd-list>
            </ip-route-interface-forwarding-list>
          </route>
        </ip>
      </native>
    </config>
    """


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def push_config():

    payload = get_payload()

    task = sys.argv[1] if len(sys.argv) > 1 else "task7"
    mode, data = select_task(task)

    if mode is None:
        exit()

    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={"name": "iosxe"}
    ) as m:

        print("\n Connected")

        # -----------------------------
        # 1. CAPABILITIES CHECK
        # -----------------------------
        print("\n=== SERVER CAPABILITIES ===")
        for cap in m.server_capabilities:
            print(cap)

        use_candidate = any(":candidate" in cap for cap in m.server_capabilities)
        use_confirmed = any(":confirmed-commit" in cap for cap in m.server_capabilities)

        if use_candidate:
            print("\n Candidate supported")
            target_ds = "candidate"
        else:
            print("\n Candidate NOT supported → using running")
            target_ds = "running"

        # -----------------------------
        # 2. LOCK (ALLEEN ALS KAN)
        # -----------------------------
        if use_candidate:
            print("\n Locking candidate datastore...")
            lock = m.lock(target="candidate")
            print(parse_reply(str(lock)))
        else:
            print("\n Skipping lock (no candidate)")

        try:
            # -----------------------------
            # 3. PUSH CONFIG
            # -----------------------------
            print("\n Sending config...")
            response = m.edit_config(
                target=target_ds,
                config=payload
            )

            print(pretty_xml(str(response)))
            print(parse_reply(str(response)))

            # -----------------------------
            # 4. VALIDATE
            # -----------------------------
            if use_candidate:
                print("\n Validating candidate...")
                try:
                    val = m.validate(source="candidate")
                    print(pretty_xml(str(val)))
                except Exception as e:
                    print(f" Validation not supported: {e}")
            else:
                print("\n Skipping validation")

            # -----------------------------
            # 5. COMMIT
            # -----------------------------
            if use_candidate:
                if use_confirmed:
                    print("\n Commit confirmed (30 sec rollback timer)")
                    m.commit(confirmed=True, timeout=30)

                    input("\n Druk ENTER om commit definitief te maken...")

                print("\n Final commit...")
                commit = m.commit()
                print(parse_reply(str(commit)))

            else:
                print("\n Config direct toegepast op running")

        except Exception as e:
            print(f"\n FOUT: {e}")

            if use_candidate:
                print("\n↩ Rollback (discard changes)")
                m.discard_changes()

        finally:
            # -----------------------------
            # 6. UNLOCK
            # -----------------------------
            if use_candidate:
                print("\n Unlocking datastore...")
                unlock = m.unlock(target="candidate")
                print(parse_reply(str(unlock)))



def select_task(task_name):

    if task_name == "task7":
        return "CONFIG", task7_hostname()

    elif task_name == "get_interfaces":
        return "GET", get_interfaces_filter()

    elif task_name == "get_running":
        return "GET_CONFIG", None

    else:
        print(" Unknown task")
        return None, None
    
# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    push_config()