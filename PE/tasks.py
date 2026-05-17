def task1_interface_description():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>0/0/0</name>
            <description xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">Geconfigureerd via netconf en python</description>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task2_interface_enable():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>0/0/0</name>
            <shutdown xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge"/>
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
            <name>0/0/0</name>
            <ip>
              <address>
                <primary>
                  <address xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">10.3.3.3</address>
                  <mask xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">255.255.255.0</mask>
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
          <GigabitEthernet>
            <name>0/0/0</name>
            <ip>
              <address>
                <primary nc:operation="remove" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                </primary>
              </address>
            </ip>
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
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>33</name>
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
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>33</name>
            <ip>
              <address>
                <primary>
                  <address nc:operation="merge">10.10.10.10</address>
                  <mask nc:operation="merge">255.255.255.0</mask>
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
        <hostname xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">LAB-RA03-C01-R01</hostname>
      </native>
    </config>
    """
def task8_dns():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <name-server>
            <vrf xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
              <word>google</word>
              <server-ip nc:operation="merge">10.199.64.66</server-ip>
            </vrf>
          </name-server>
        </ip>
      </native>
    """
def task9_ntp():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ntp>
          <server xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ntp">
            <ip>
              <source xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">10.199.64.66</source>
            </ip>
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
          <ip-route-interface-forwarding-list xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <prefix>0.0.0.0</prefix>
            <mask>0.0.0.0</mask>
            <fwd-list>
              <fwd>10.199.65.100</fwd>
            </fwd-list>
          </ip-route-interface-forwarding-list>
        </route>
      </ip>
    </native>
  </config>
    """

def task11_no_static_route():
    return """
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <ip>
        <route>
          <ip-route-interface-forwarding-list xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
            <prefix>0.0.0.0</prefix>
            <mask>0.0.0.0</mask>
            <fwd-list>
              <fwd>10.199.65.100</fwd>
            </fwd-list>
          </ip-route-interface-forwarding-list>
        </route>
      </ip>
    </native>
  </config>
    """

def task12_motd():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
          <motd>
            <banner xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">Welkom, via netconf</banner>
          </motd>
        </banner>
      </native>
    </config>
    """

def task13_create_local_user():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
          <name>pippo</name>
          <privilege nc:operation="merge">15</privilege>
        </username>
      </native>
    </config>
    """
def task14_mod_user_password():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
          <name>pippo</name>
          <privilege>15</privilege>
          <password>
            <password>declown</password>
          </password>
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
            <COMMUNITY>
              <name>public</name>
              <ro/>
            </COMMUNITY>
            <COMMUNITY>
              <name>private</name>
              <rw/>
            </COMMUNITY>
          </community>
        </snmp-server>
      </native>
    </config>
    """
def task19_running_config():
    return """
    <nc:filter type="subtree" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      </native>
    </nc:filter>
    """

def task20_val_config():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>33</name>
            <ip>
              <address>
                <primary>
                  <address nc:operation="merge">20.20.20.20</address>
                  <mask nc:operation="merge">255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """
def task21_ds_candidate_com_if():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>33</name>
            <ip>
              <address>
                <primary>
                  <address nc:operation="merge">21.21.21.21</address>
                  <mask nc:operation="merge">255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """

def task22_ds_lock_unlock():
        return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>33</name>
            <ip>
              <address>
                <primary>
                  <address nc:operation="merge">22.22.22.22</address>
                  <mask nc:operation="merge">255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """

def task23_multi_if():
        return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>66</name>
            <description>Multi-if-1-rpc</description>
            <ip>
              <address>
                <primary>
                  <address>66.66.66.66</address>
                  <mask>255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>99</name>
            <description>Multi-if-1-rpc</description>
            <ip>
              <address>
                <primary>
                  <address>99.99.99.99</address>
                  <mask>255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
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


def tak26_ipv6():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>777</name>
            <description>IPv6 instellen via netconf</description>
            <ipv6>
              <address>
                <link-local-address>
                  <address>FE80::1</address>
                  <link-local nc:operation="merge"/>
                </link-local-address>
              </address>
            </ipv6>
          </Loopback>
        </interface>
      </native>
    </config>
    """

def task27_ospf():
         return """
<config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <router>
          <ospf>
            <id>1</id>
            <network>
              <ip>192.168.10.0</ip>
              <mask>0.0.0.255</mask>
              <area>0</area>
            </network>
          </ospf>
        </router>
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