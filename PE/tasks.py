# Geverifieerd te werken op vrouter, if aangepast voor lab

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
# Geverifieerd te werken op vrouter, if aangepast voor lab
def task2_interface_enable():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>0/0/0</name>
            <shutdown xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
# Geverifieerd te werken op vrouter, if aangepast voor lab
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
                  <address xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">10.3.3.4</address>
                  <mask xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
# Geverifieerd te werken op vrouter, if aangepast voor lab
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
# Geverifieerd te werken op vrouter, if aangepast voor lab
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
# Geverifieerd te werken op vrouter, if aangepast voor lab
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
# Geverifieerd te werken op vrouter, if aangepast voor lab
def task7_set_hostname():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">LAB-RA03-C01-R01</hostname>
      </native>
    </config>
    """
# Geverifieerd te werken op vrouter, if aangepast voor lab
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
    </config>
    """
def task9_ntp():
    return """
<config>
  <ntp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ntp">
    <server-list>
      <ip-address>10.199.64.66</ip-address>
    </server-list>
  </ntp>
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
            <id>31</id>
            <name>Management</name>
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
            <name>31</name>
            <ip>
              <address>
                <primary>
                  <address>1172.17.3.4</address>
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
    <interface>
      <Loopback>
        <name>66</name>
        <description>Loopback OSPF 1</description>
        <ip>
          <address>
            <primary>
              <address>17.17.17.17</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
      <Loopback>
        <name>99</name>
        <description>Loopback OSPF 2</description>
        <ip>
          <address>
            <primary>
              <address>19.19.19.19</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
    <router>
      <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
        <id>1</id>
        <network>
          <ip>17.17.17.0</ip>
          <mask>0.0.0.255</mask>
          <area>0</area>
        </network>
        <network>
          <ip>19.19.19.0</ip>
          <mask>0.0.0.255</mask>
          <area>0</area>
        </network>
        <passive-interface>
          <interface>default</interface>
        </passive-interface>
      </ospf>
    </router>
  </native>
</config>
    """
""" <config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>66</name>
        <description>Loopback OSPF 1</description>
        <ip>
          <address>
            <primary>
              <address>17.17.17.17</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
      <Loopback>
        <name>99</name>
        <description>Loopback OSPF 2</description>
        <ip>
          <address>
            <primary>
              <address>19.19.19.19</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
    <router>
      <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
        <id>1</id>
        <network>
          <ip>17.17.17.0</ip>
          <mask>0.0.0.255</mask>
          <area>0</area>
        </network>
        <network>
          <ip>19.19.19.0</ip>
          <mask>0.0.0.255</mask>
          <area>0</area>
        </network>
        <passive-interface>
          <interface>default</interface>
        </passive-interface>
        <passive-interface>
          <interface>GigabitEthernet0/0/0</interface>
          <no-passive/>
        </passive-interface>
      </ospf>
    </router>
  </native>
</config> """


def task28_routing():
         return """
    <filter>
      <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>
    </filter>
    """

def task29_MTU():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>0/0/0</name>
            <ip>
              <mtu xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">1800</mtu>
            </ip>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """

def task30_acl():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <access-list>
            <extended xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
              <name>met-netconf</name>
              <access-list-seq-rule>
                <sequence>10</sequence>
                <ace-rule>
                  <action>permit</action>
                  <protocol>ip</protocol>
                  <any/>
                  <dst-any/>
                </ace-rule>
              </access-list-seq-rule>
            </extended>
          </access-list>
        </ip>
        <interface>
          <GigabitEthernet>
            <name>0/0/0</name>
            <ip>
              <access-group>
                <in>
                  <acl>
                    <acl-name>met-netconf</acl-name>
                    <in/>
                  </acl>
                </in>
              </access-group>
            </ip>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """

def task31_speed_duplex():
         return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
            <name>1</name>
            <speed xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet" nc:operation="merge">
              <value-1000 nc:operation="merge"/>
              <nonegotiate/>
            </speed>
            <duplex xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet" nc:operation="merge">full</duplex>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """

def task32_yang_actions():
         return """
  <clear xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interface>GigabitEthernet1</interface>
  </clear>
    """

def task34_openCONFIG():
          return """
<config>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>Loopback999</name>
      <config>
        <name>Loopback999</name>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
          ianaift:softwareLoopback
        </type>
        <enabled>true</enabled>
        <description>Loopbackvia openconf</description>
      </config>
      <subinterfaces>
        <subinterface>
          <index>0</index>
          <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
            <addresses>
              <address>
                <ip>9.9.9.9</ip>
                <config>
                  <ip>9.9.9.9</ip>
                  <prefix-length>24</prefix-length>
                </config>
              </address>
            </addresses>
          </ipv4>
        </subinterface>
      </subinterfaces>
    </interface>
  </interfaces>
</config>
    """

def task35_full_deploy():
          return """
  <config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ip>
      <access-list>
        <extended xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
          <name>met-netconf</name>
          <access-list-seq-rule>
            <sequence>10</sequence>
            <ace-rule>
              <action>permit</action>
              <protocol>ip</protocol>
              <any/>
              <dst-any/>
            </ace-rule>
          </access-list-seq-rule>
        </extended>
      </access-list>
    </ip>
    <interface>
      <Loopback>
        <name>66</name>
        <description>Loopback Service 1</description>
        <ip>
          <address>
            <primary>
              <address>17.17.17.17</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
      <Loopback>
        <name>99</name>
        <description>Loopback Service 2</description>
        <ip>
          <address>
            <primary>
              <address>19.19.19.19</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
    <ip>
      <route>
        <ip-route-interface-forwarding-list>
          <prefix>0.0.0.0</prefix>
          <mask>0.0.0.0</mask>
          <fwd-list>
            <fwd>10.199.65.100</fwd>
          </fwd-list>
        </ip-route-interface-forwarding-list>
      </route>
    </ip>
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <ip>
          <access-group>
            <in>
              <acl>
                <acl-name>met-netconf</acl-name>
                <in/>
              </acl>
            </in>
          </access-group>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
</config>
    """

def task36_end_to_end():
     return """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <hostname>NETCONF-RUNNER-TAAK36</hostname>
    <interface>
      <Loopback>
        <name>66</name>
        <description>Loopback OSPF 1</description>
        <ip>
          <address>
            <primary>
              <address>17.17.17.17</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
      <Loopback>
        <name>99</name>
        <description>Loopback OSPF 2</description>
        <ip>
          <address>
            <primary>
              <address>19.19.19.19</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
    <router>
      <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
        <id>1</id>
        <network>
          <ip>17.17.17.0</ip>
          <mask>0.0.0.255</mask>
          <area>0</area>
        </network>
        <network>
          <ip>19.19.19.0</ip>
          <mask>0.0.0.255</mask>
          <area>0</area>
        </network>
        <passive-interface>
          <interface>default</interface>
        </passive-interface>
      </ospf>
    </router>
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
