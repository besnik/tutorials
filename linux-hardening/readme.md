# Linux Hardening

This document discusses how to improve configuration of your server so it is more secure. 
The concepts are general and can be applied also on Windows server.

## SSH Hardening

Change SSH port (22) and disable root login.

`sudo nano -w /etc/ssh/sshd_config`

Change the following lines (1234 port is just example, set new ssh port number as you like):

```
Port 1234
PermitRootLogin no
```

Restart SSH

```
sudo /etc/init.d/ssh restart
```

## Firewall - UFW

Install if not present in the system:

`sudo apt-get install ufw`

Check status, by default it is disabled on ubuntu:

`sudo ufw status verbose`

Allow SSH, Http, Https services (only allow those that you really need, by default you want at least SSH and HTTP):

```
sudo ufw allow 1234   # use 22 if you did not change SSH port (see SSH hardening section)
sudo ufw allow 80     # http
sudo ufw allow 443    # https
```

Enable Firewall

`sudo ufw enable`

## Secure shared memory - fstab

`/dev/shm` can be used in an attack against a running service, such as httpd. Modify `/etc/fstab` to make it more secure.

Enter the following:

`sudo nano -w /etc/fstab`

Add the following line to the bottom and save (control-x). You will need to reboot for this setting to take effect:

`tmpfs     /dev/shm     tmpfs     defaults,noexec,nosuid     0     0`

## Protect su by limiting access only to admin group

To limit the use of su by admin users only we need to create an admin group, then add users and limit the use of su to the admin group.

Enter these commands to create an admin group, add your user to it and lock down `/bin/su/`:

```
sudo groupadd admin
sudo usermod -a -G admin `whoami`
sudo dpkg-statoverride --update --add root admin 4750 /bin/su
```

Note: replace ``whoami``  with username you want to add to the group `admin`.

## Harden network with sysctl settings

The `/etc/sysctl.conf` file contains settings related to your network configuration. These edits prevent some very simple attacks with very little work. 

Example configuration

```
#
# /etc/sysctl.conf - Configuration file for setting system variables
# See /etc/sysctl.d/ for additional system variables
# See sysctl.conf (5) for information.
#

# Uncomment the next two lines to enable Spoof protection (reverse-path filter)
# Turn on Source Address Verification in all interfaces to
# prevent some spoofing attacks
net.ipv4.conf.default.rp_filter=1
net.ipv4.conf.all.rp_filter=1

# Uncomment the next line to enable TCP/IP SYN cookies
net.ipv4.tcp_syncookies=1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Do not accept ICMP redirects (prevent MITM attacks)
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0 
net.ipv6.conf.default.accept_redirects = 0

# Do not send ICMP redirects (we are not a router)
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Do not accept IP source route packets (we are not a router)
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Log Martian Packets
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Ignore Directed pings
net.ipv4.icmp_echo_ignore_all = 1
```

## Scan logs and ban suspicious hosts  - Fail2ban

Fail2ban scans log files and bans IPs that look malicious. Too many password failures, seeking for exploits, etc.

Install Fail2ban:

`sudo apt-get install fail2ban`

After the install open up the `/etc/fail2ban/jail.conf` file for editing:

`sudo nano -w /etc/fail2ban/jail.conf`

Example of updated configuration of `# Jails` section:

```
[ssh]

enabled  = true
port     = 888
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 6

[ssh-ddos]

enabled  = true
port     = 8888
filter   = sshd-ddos
logpath  = /var/log/auth.log
maxretry = 10

[recidive]

enabled  = true
filter   = recidive
logpath  = /var/log/fail2ban.log
action   = iptables-allports[name=recidive]
       sendmail-whois-lines[name=recidive, logpath=/var/log/fail2ban.log]
bantime  = 604800  ; 1 week
findtime = 86400   ; 1 day
maxretry = 5
```

Restart Fail2ban

`sudo /etc/init.d/fail2ban restart`

# Further reading

The above content was created also using following articles:

 - http://0v.org/installing-ghost-on-ubuntu-nginx-and-mysql/
