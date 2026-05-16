import sys
from ncclient import manager
import xml.dom.minidom

from tasks import *
from filters import *


HOST = "192.168.56.105"
PORT = 830
USER = "cisco"
PASS = "cisco123!"


# -----------------------------
# PRETTY PRINT
# -----------------------------
def pretty_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")


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

    task = sys.argv[1] if len(sys.argv) > 1 else "get_hostname"
    mode, data = select_task(task)

    if mode is None:
        return

    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={"name": "iosxe"}
    ) as m:

        print("Connected")

        # -----------------------------
        # CAPABILITY CHECK
        # -----------------------------
        use_candidate = any(":candidate" in cap for cap in m.server_capabilities)

        if use_candidate:
            print("Candidate datastore supported")
            target_ds = "candidate"
        else:
            print("Using running datastore")
            target_ds = "running"

        # -----------------------------
        # READ OPERATIONS
        # -----------------------------
        if mode == "GET":
            print("Retrieving data...")
            response = m.get(filter=data)
            print(pretty_xml(str(response)))
            return

        elif mode == "GET_CONFIG":
            print("Retrieving running configuration...")
            response = m.get_config(source="running")
            print(pretty_xml(str(response)))
            return

        # -----------------------------
        # WRITE OPERATIONS
        # -----------------------------
        elif mode == "CONFIG":

            payload = data

            if use_candidate:
                print("Locking candidate datastore")
                m.lock(target="candidate")

            try:
                print("Sending configuration")

                response = m.edit_config(
                    target=target_ds,
                    config=payload
                )

                print(pretty_xml(str(response)))

                if use_candidate:
                    print("Committing configuration")
                    m.commit()
                else:
                    print("Configuration applied directly to running")

            except Exception as e:
                print("Error:", e)

                if use_candidate:
                    print("Discarding changes")
                    m.discard_changes()

            finally:
                if use_candidate:
                    print("Unlocking datastore")
                    m.unlock(target="candidate")


# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    main()