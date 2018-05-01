#!/bin/bash

UPTIME_DAYS=$(expr `cat /proc/uptime | cut -d '.' -f1` % 31556926 / 86400)
UPTIME_HOURS=$(expr `cat /proc/uptime | cut -d '.' -f1` % 31556926 % 86400 / 3600)
UPTIME_MINUTES=$(expr `cat /proc/uptime | cut -d '.' -f1` % 31556926 % 86400 % 3600 / 60)

POOLLIST=$(zpool status | grep pool: | awk '{print $2}')

red='\e[00;31m'
blue='\e[01;34m'
normal='\e[00;00m'
yellow='\e[00;33m'
cyan='\e[01;96m'

# ┃ ╋ ┗ ┏ ┛ ━ ┓
echo -e "${blue}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo -e "${blue}┃┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ${normal}SERVER INFO ${blue}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓┃"
echo ""
echo -e "   ${yellow}Hostname :${normal} $HOSTNAME"
echo -e "   ${yellow}Distrib. :${normal} `lsb_release -s -d` `uname -r`"
echo -e "   ${yellow}Uptime   :${normal} $UPTIME_DAYS days $UPTIME_HOURS hours $UPTIME_MINUTES minutes"
echo ""
echo -e "   ${yellow}CPU  :${normal}`cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d':' -f2`"
echo -e "   ${yellow}RAM  :${normal}`free -m | grep Mem: | awk '{printf " Total: %0.2f GB | Used: %0.2f GB | Free: %0.2f GB\n",($2/1024),($3/1024),($4/1024);}'`"
echo -e "   ${yellow}Swap :${normal}`free -m | grep Swap: | awk '{printf " Total: %0.2f GB | Used: %0.2f GB | Free: %0.2f GB\n",($2/1024),($3/1024),($4/1024);}'`"
echo ""
echo -e "   ${yellow}Load Average :${normal} `cat /proc/loadavg | awk '{print $1 ", " $2 ", " $3}'`"
echo ""
echo -e "   ${yellow}Disk usage :${normal}"
echo ""
echo -e "${cyan}ZFS_Pool Total_Size Used Free Frag Cap Dedup\n${normal}`for POOL in $POOLLIST; do zpool list $POOL | grep -v NAME | awk '{print $1, $2, $3, $4, $6, $7, $8}'; done`" | column -t | awk '{print "     ", $0}'
#echo -e "${cyan}ZFS_Pool Total_Size Used Free Frag Cap Dedup\n${normal}`for POOL in $POOLLIST; do zfs list $POOL | grep -v NAME | awk '{printf "%-10.10s %10.5s %10.5s\n",$1, $3, $2}'; done`" | column -t | awk '{print "     ", $0}'
echo -e ""
echo -e "${cyan}ZFS_Datasets\n${normal}`zfs list -o name,used,usedsnap,avail,mountpoint -d 2`" | column -t | awk '{print "     ", $0}'
echo ""
echo -e "   ${yellow}IP Addresses :${normal}"
echo "" 
echo -e "`ip a | grep inet | awk '{print ($5=="lo")? $5 : $7, ":", $2}' | awk '{print "     ", $0}'`"
echo ""
echo -e "${blue}┃┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛┃${normal}"
echo -e "${blue}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${normal}"
