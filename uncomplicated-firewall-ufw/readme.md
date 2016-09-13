# UFW - Uncomplicated Firewall

The default firewall configuration tool for Ubuntu is `ufw`. 
Developed to ease `iptables` firewall configuration, `ufw` provides a user friendly way to create 
an IPv4 or IPv6 host-based firewall. By default UFW is disabled.

Community documentation: https://help.ubuntu.com/community/UFW

# Start, Stop and Check Status

To check the status of UFW:

`sudo ufw status verbose`

To turn UFW on with the default set of rules:

`sudo ufw enable`

To disable ufw use:

`sudo ufw disable`

Show firewall report:

`sudo ufw show raw`

# Allow and Deny

Allow:

`sudo ufw allow <port>/<optional: protocol>`

Examples:

```
sudo ufw allow 1010
sudo ufw allow 80
sudo ufw allow 53/tcp
sudo ufw allow 53/udp
```

Deny:

`sudo ufw deny <port>/<optional: protocol>`

Examples:

```
sudo ufw deny 53
sudo ufw deny 53/tcp
```

# Delete existing rules

To delete a rule, simply prefix the original rule with delete.

`sudo ufw delete deny 80/tcp`

# Allow & Deny by IP Address

Allow by IP address:

`sudo ufw allow from <ip address>`

Allow by Subnet:

`sudo ufw allow from 192.168.1.0/24`

Allow by specific port and IP address:

`sudo ufw allow from <target> to <destination> port <port number>`

Example (allow IP address 192.168.0.4 access to port 22 for all protocols):

`sudo ufw allow from 192.168.0.4 to any port 22`

Allow by specific port, IP address and protocol

`sudo ufw allow from <target> to <destination> port <port number> proto <protocol name>`

example: allow IP address 192.168.0.4 access to port 22 using TCP

`sudo ufw allow from 192.168.0.4 to any port 22 proto tcp`

Deny by specific IP:

`sudo ufw deny from <ip address>`

Deny by specific port and IP address:

`sudo ufw deny from <ip address> to <protocol> port <port number>`

# Allow & Deny Services (e.g. SSH or NGINX)

You can also allow or deny by service name since ufw reads from `/etc/services` To see get a list of services:

`less /etc/services`

or

`sudo ufw app list`

Allow:

`sudo ufw allow <service name>`

Example:

```
sudo ufw allow ssh
sudo ufw allow 'Nginx HTTP'
```

Deny:

`sudo ufw deny <service name>`

Example:

`sudo ufw deny ssh`

# Logging

To enable logging use:

`sudo ufw logging on`

To disable logging use:

`sudo ufw logging off`

# Enable PING

In order to disable ping (icmp) requests, you need to edit `/etc/ufw/before.rules` and remove the following lines:

```
# ok icmp codes
-A ufw-before-input -p icmp --icmp-type destination-unreachable -j ACCEPT
-A ufw-before-input -p icmp --icmp-type source-quench -j ACCEPT
-A ufw-before-input -p icmp --icmp-type time-exceeded -j ACCEPT
-A ufw-before-input -p icmp --icmp-type parameter-problem -j ACCEPT
-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT
```

or change the "ACCEPT" to "DROP" 

```
# ok icmp codes
-A ufw-before-input -p icmp --icmp-type destination-unreachable -j DROP
-A ufw-before-input -p icmp --icmp-type source-quench -j DROP
-A ufw-before-input -p icmp --icmp-type time-exceeded -j DROP
-A ufw-before-input -p icmp --icmp-type parameter-problem -j DROP
-A ufw-before-input -p icmp --icmp-type echo-request -j DROP
```

# Numbered rules

Listing rules with a reference number

You may use status numbered to show the order and id number of rules:

`sudo ufw status numbered`

Editing numbered rules.

You may then delete rules using the number. This will delete the first rule and rules will shift up to fill in the list.

`sudo ufw delete 1`

Insert numbered rule

`sudo ufw insert 1 allow from <ip address>`

# Further reading

 - `man ufw`
 - https://help.ubuntu.com/community/UFW
 - http://0v.org/installing-ghost-on-ubuntu-nginx-and-mysql/