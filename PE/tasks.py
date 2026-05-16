def task1_interface_description()
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1</name>
            <description>Configured via NETCONF</description>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task2_interface_enable()
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1</name>
            <shutdown>false</shutdown>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task3_set_ipv4():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1</name>
            <ip>
              <address>
                <primary>
                  <address>192.168.1.1</address>
                  <mask>255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task4_remove_ipv4():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet operation="merge">
            <name>1</name>
            <ip operation="delete"/>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task5_create_loopback():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>10</name>
          </Loopback>
        </interface>
      </native>
    </config>
    """
def task6_loopback_ip():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>10</name>
            <ip>
              <address>
                <primary>
                  <address>10.10.10.1</address>
                  <mask>255.255.255.255</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """
def task7_set_hostname():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>NETCONF-Router</hostname>
      </native>
    </config>
    """
def task8_dns():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <name-server>8.8.8.8</name-server>
        </ip>
      </native>
    </config>
    """
def task9_ntp():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ntp>
          <server>
            <server-list>
              <ip-address>192.168.1.100</ip-address>
            </server-list>
          </server>
        </ntp>
      </native>
    </config>
    """
def task10_static_route():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <route>
            <ip-route-interface-forwarding-list>
              <prefix>10.0.0.0</prefix>
              <mask>255.255.255.0</mask>
              <fwd-list>
                <fwd>192.168.1.254</fwd>
              </fwd-list>
            </ip-route-interface-forwarding-list>
          </route>
        </ip>
      </native>
    </config>
    """

def task11_no_static_route():
    return """
    <config>"""

def task12_motd():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
          <motd>
            <banner>Welcome to the NETCONF Router</banner>
          </motd>
        </banner>
      </native>
    </config>
    """

def task13_create_local_user():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username>
          <name>netconf-user</name>
          <password>netconf-pass</password>
        </username>
      </native>
    </config>
    """
def task14_mod_user_password():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username>
          <name>netconf-user</name>
          <password>new-netconf-pass</password>
        </username>
      </native>
    </config>
    """

def task15_create_vlan():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <vlan>
          <vlan-list>
            <id>10</id>
            <name>NETCONF_VLAN</name>
          </vlan-list>
        </vlan>
      </native>
    </config>
    """

def task16_vlan_interface():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Vlan>
            <name>10</name>
            <ip>
              <address>
                <primary>
                  <address>10.10.10.2</address>
                  <mask>255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Vlan>
        </interface>
      </native>
    </config>
    """
def task17_snmp():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <snmp-server>
          <community>
            <name>public</name>
            <authorization>ro</authorization>
          </community>
        </snmp-server>
      </native>
    </config>
    """
def task18_if_stats():
    return """
    <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name/>
          <statistics/>
        </interface>
      </interfaces-state>
    </filter>
    """
def task19_running_config():
    return None  # geen filter nodig, we willen alles zien

def task20_val_config():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        ...
      </native>
    </config>
    """
def task21_ds_candidate_com_if():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task22_ds_lock_unlock():
        return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task23_multi_if():
        return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task24_rollback():
        return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task25_diff_run_cand():
        return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def tak26_ipv6():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task27_ospf():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task28_routing():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task29_MTU():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task30_acl():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task31_speed_duplex():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task32_yang_actions():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task34_openCONFIG():
          return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def task35_full_deploy():
          return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      ...
      </native>
    </config>
    """

def get_interfaces_and_hostname():
    return """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname/>
      </native>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name/>
          <enabled/>
        </interface>
      </interfaces>
    </filter>
    """