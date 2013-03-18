
======================
Swift Interface Header
======================

A middleware to set the header HTTP_X_INTERFACE to a value defined in rule configuration                                        

*******
Install
*******

pip install https://github.com/enovance/swift-interface-header/zipball/master

*************
Configuration
*************

In /etc/swift/proxy-server.conf on the main pipeline add "interface_header"

[filter:interface_header]
use = egg:swift_interface_header#interface_header

# Some optionnal configuration to fill the header "HTTP_X_INTERFACE" in
# fonction of data in the request environment
interface_default = int
interface_rule_1 = HTTP_HOST, 123.123.123.123:8080, ext
interface_rule_2 = SERVER_PORT, 8081, ext
interface_rule_3 = SERVER_NAME, 192.168.3.51, ext
