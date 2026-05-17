# 🟢 HULK v2.4 – NETCONF Task Executor

Een krachtige NETCONF automation tool geschreven in Python voor het uitvoeren van netwerkconfiguraties, validaties en monitoring via YANG-modellen.

Dit script automatiseert configuraties op netwerkapparaten (zoals Cisco IOS-XE) en biedt ondersteuning voor:

✅ Config push (edit-config)  
✅ Data retrieval (get / get-config)  
✅ Candidate / running datastore handling  
✅ Rollback & diff vergelijking  
✅ YANG-aware parsing  
✅ Logging (tekst + JSON)  
✅ Remote config ophalen via GitHub  

---

## 📦 Features

### 🔧 NETCONF Operaties
- GET → informatie ophalen van het toestel  
- CONFIG → configuraties uitvoeren  
- ROLLBACK → rollback uitvoeren  
- COMPARE → running vs candidate vergelijken  
- CAPABILITIES → device capabilities tonen  
- ACTION → RPC acties uitvoeren  

---

## 📊 Logging & Monitoring

Logs worden opgeslagen in:

```
logs/netconf_.log
logs/netconf_output.json
```

JSON logging bevat:
- timestamp  
- task naam  
- status (SUCCESS / ERROR / UNKNOWN)  
- details  

---

## 📡 YANG ondersteuning

- Extractie van gebruikte YANG modules uit XML  
- Overzicht van gebruikte namespaces  
- Debugging van payloads  

---

## 📦 Voorbeeld payload

```xml
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>0/0/0</name>
        <description xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
          Geconfigureerd via netconf en python
        </description>
      </GigabitEthernet>
    </interface>
  </native>
</config>
```

---

## ✅ Voorbeeld uitvoering (NETCONF)

screenshots/get_hostname.png

---

## 🚀 CI/CD Deployment (GitHub Actions)

### Pipeline overzicht
screenshots/github_pipeline.png

### Pipeline logs
screenshots/github_logs.png

---

## 📁 Projectstructuur

```
hulk.py
tasks.py
filters.py
netconf-hulk-requirements.txt
36_end_to_end_config.xml
logs/
screenshots/
```

---

## ▶️ Gebruik

```
python main.py <device> <mode> <tasks>
```

---

## 📋 Overzicht van taken

| Task   | Beschrijving |
|--------|-------------|
| task1  | Interface description instellen |
| task2  | Interface inschakelen |
| task3  | IPv4 configuratie |
| task4  | IPv4 verwijderen |
| task5  | Loopback interface |
| task6  | Loopback IPv4 |
| task7  | Hostname instellen |
| task8  | DNS configuratie |
| task9  | NTP configuratie |
| task10 | Static route |
| task11 | Static route verwijderen |
| task12 | MOTD banner |
| task13 | User aanmaken |
| task14 | Password wijzigen |
| task15 | VLAN |
| task16 | VLAN interface |
| task17 | SNMP |
| task18 | Interface statistics |
| task19 | Running config |
| task20 | Config valideren |
| task21 | Candidate commit |
| task22 | Lock/unlock |
| task23 | Multi config |
| task24 | Script logica |
| task25 | Script logica |
| task26 | IPv6 |
| task27 | OSPF |
| task28 | Routing info |
| task29 | MTU |
| task30 | ACL |
| task31 | Speed/duplex (niet werkend) |
| task32 | Clear counters |
| task33 | Capabilities |
| task34 | OpenConfig |
| task35 | Full deployment |
| task36 | End-to-end |

---

## 👨‍💻 Auteur

Manuel Sperti


## 🔄 Flow Diagram (Mermaid)

```mermaid
flowchart TD

A[Start script] --> B[Lees CLI args]
B --> C[Select device + env vars]
C --> D[Maak NETCONF connectie]

D --> E[Bepaal datastore mode]
E --> F[Loop door tasks]

F --> G{Task type?}

G -->|GET| H["Run m.get()"]
G -->|CONFIG| I[Backup running config]
I --> J{Candidate supported?}

J -->|Yes| K[Lock candidate]
K --> L[edit-config]
L --> M[validate + commit]
M --> N[unlock]

J -->|No| O[edit-config -> running]

G -->|CAPABILITIES| P[Print capabilities]
G -->|ROLLBACK| Q[Restore backup]
G -->|COMPARE| R[Diff running vs candidate]
G -->|ACTION| S[Execute RPC dispatch]

H --> T[Print response]
N --> T
O --> T
P --> F
Q --> F
R --> F
S --> T

T --> U[Interpret response]
U --> F

F --> V{Meer tasks?}
V -->|Yes| F
V -->|No| W[Save JSON logs]

W --> X[End]