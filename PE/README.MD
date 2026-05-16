# NETCONF Automation Script
Dit Python-script maakt verbinding met netwerkapparaten via NETCONF en laat toe om zowel lees- (GET) als schrijfoperaties (CONFIG) uit te voeren.
Het script is modulair opgebouwd en gebruikt externe modules (tasks en filters) om configuraties en data-opvragingen flexibel te beheren.

### 📌 Features

✅ Verbinding maken met NETCONF-capable devices (bv. Cisco IOS-XE)
✅ Ondersteuning voor meerdere apparaten (vrouter, labrouter, labswitch)
✅ Ondersteunt:

GET (operationele data)
GET_CONFIG (configuratie ophalen)
CONFIG (configuraties aanpassen)


✅ Automatische detectie van candidate datastore
✅ Veilige configuratie (lock / commit / rollback)
✅ XML pretty-print voor leesbare output
✅ Modulair uitbreidbaar via tasks.py en filters.py


## 📂 Projectstructuur

- main.py — Hoofdscript (NETCONF client)
- tasks.py — XML-configuraties (write taken)
- filters.py — XML-filters (read taken)
- README.md — Documentatie


### ⚙️ Vereisten
Installeer de benodigde Python library:
Shell pip install ncclientShow more lines

### 🔐 Environment Variables
De verbindingsgegevens worden niet hardcoded, maar via environment variables ingesteld:
Voorbeeld (Linux / macOS)
Shell
export VROUTER_IP=192.168.1.1
export VROUTER_USER=admin
export VROUTER_PASS=password

### Ondersteunde apparaten

Device                          Environment Variables
vrouter                         VROUTER_IP, VROUTER_USER, VROUTER_PASS
labrouter                       LAB_ROUTER_IP, LAB_ROUTER_USER, LAB_ROUTER_PASS
labswitch                       LAB_SWITCH_IP, LAB_SWITCH_USER, LAB_SWITCH_PASS


### 🚀 Gebruik
#### Basisgebruik
Shellpython main.pyShow more lines
##### Voorbeeld
Shell python main.py vrouter get_hostname get_motd

##### Zonder arguments
Shell python main.pyShow

#### ➡️ Standaard worden uitgevoerd:

get_hostname
get_motd


## 📋 Beschikbare Taken
### 🔍 Read Tasks


Task                Beschrijving
get_interfaces      Haalt interface-informatie op
get_running         Volledige running-config
get_hostname        Hostname ophalen
get_motd            Message of the Day ophalen

### ✏️ Write Tasks (CONFIG)

Task                Beschrijving
task1               Interface beschrijving aanpassen
task7               Hostname configureren
task10              Static route toevoegen
set_hostname        Nieuwe hostname instellen

### ⚙️ Hoe het script werkt

#### 1. Device selectie
Het script kiest het apparaat op basis van het eerste argument:

Python device = sys.argv[1]

Afhankelijk daarvan worden de juiste credentials geladen uit environment variables.

#### 2. NETCONF verbinding
python with manager.connect(...)

Verbindt via poort 830
Gebruikt ncclient
Device type: iosxe


#### 3. Capability detectie
Python use_candidate = any(":candidate" in cap for cap in m.server_capabilities)

➡️ Bepaalt of het device een candidate datastore ondersteunt.

Scenario            Gedrag
✅ Candidate        lock → edit → commit
❌ Geen             direct naar running config

#### 4. Task selectie
Python mode, data = select_task(task)

Elke taak wordt vertaald naar:

Mode: GET, GET_CONFIG, CONFIG
Data: XML payload of filter


#### 5. Read operaties

##### GET (operationele data)
Python m.get(filter=data)

##### GET_CONFIG
Python m.get_config(source="running")
➡️ Output wordt geformatteerd via:
Python pretty_xml()

#### 6. Write operaties
Python m.edit_config(target=target_ds, config=data)
##### Workflow:
###### Als candidate:

Lock datastore
Config sturen
Commit
Unlock

Bij fout:
Python m.discard_changes()

### 🔄 Error Handling
Bij fouten tijdens CONFIG:

Exception wordt opgevangen
Bij candidate:

❌ changes worden teruggedraaid (discard_changes)

Datastore wordt altijd ontgrendeld (finally)

### 🧩 Modulariteit
#### tasks.py
Bevat XML-configuraties:
Python def task7_hostname():    return "<config>...</config>"

### filters.py
Bevat XML filters:
Pythondef get_hostname_filter():    return "<filter>...</filter>"

➡️ Nieuwe taken toevoegen = eenvoudig uitbreiden

### 🧪 Voorbeelden
Hostname ophalen
Shell python main.py vrouter get_hostname

Interface info bekijken
Shell python main.py labrouter get_interfaces

Config wijzigen
Shell python main.py labswitch set_hostname

### ⚠️ Belangrijke opmerkingen

Zorg dat NETCONF geactiveerd is op je device:

Shell netconf-yangShow more lines

Gebruik geen hardcoded credentials (veiligheid!)
Test eerst in labomgeving


### ✅ Toekomstige uitbreidingen

CLI argument parsing (argparse)
Logging toevoegen
YAML config file
Multi-device automation
Parallel execution
RESTCONF

### 👨‍💻 Auteur
Manuel Sperti