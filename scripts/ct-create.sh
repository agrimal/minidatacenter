#!/bin/bash

source $(dirname $0)/vars

usage() {
    cat << EOF
    ==========================================
    | $0
    ==========================================
    -h|--help : Display this help
    -n|--name <NAME> : Name of the container
    -c|--cpu  <CPU> : Number of CPU cores
    -m|--mem  <MEMORY{KB,MB,GB}> : Quantity of RAM
    -i|--$ETH_NAME_INT <CIDR_IP_ADDRESS> : CIDR IP Address for $ETH_NAME_INT
    -e|--$ETH_NAME_EXT <CIDR_IP_ADDRESS> : CIDR IP Address for $ETH_NAME_EXT
    -g|--gateway <IP_ADDRESS> : IP Address of the gateway for $ETH_NAME_EXT
    -D|--dns1 <IP_ADDRESS> : IP Address of DNS1
    -d|--dns2 <IP_ADDRESS> : IP Address of DNS2
    -I|--image <BASE_IMAGE> : LXC Image name
    -r|--directory <DIRECTORY> : Base template directory
    ==========================================
    | Example :
    | $0 --name=$BASE_CT --cpu=$BASE_CPU --mem=$BASE_MEMORY \ 
    |  --$ETH_NAME_INT=$ETHINT --$ETH_NAME_EXT=$ETHEXT \ 
    |  --gateway=$GATEWAY --dns1=$DNS_ETHEXT --dns2=$DNS_ETHINT \ 
    |  --image=$BASE_IMAGE --directory=${BASE_DIR}/$BASE_CT
    ==========================================
EOF
}

OPTIONS=$(getopt -o h,n:,c:,m:,i:,e:,g:,D:,d:,I:,r: -l help,name:,cpu:,mem:,$ETH_NAME_INT:,$ETH_NAME_EXT:,gateway:,dns1:,dns2:,image:,directory: -- "$@")

if [ $? != 0 ]; then
    echo "Error during options parsing. Aborting..."
    usage
    exit 1
fi

eval set -- "$OPTIONS"

while true; do
    case "$1" in
        -h|--help)
            usage
            exit 0;;
        -n|--name)
            BASE_CT=$2
            shift;;
        -c|--cpu)
            BASE_CPU=$2
            shift;;
        -m|--mem)
            BASE_MEMORY=$2
            shift;;
        -i|--$ETH_NAME_INT)
            ETHINT=$2
            shift;;
        -e|--$ETH_NAME_EXT)
            ETHEXT=$2
            shift;;
        -g|--gateway)
            GATEWAY=$2
            shift;;
        -D|--dns1)
            DNS_ETHEXT=$2
            shift;;
        -d|--dns2)
            DNS_ETHINT=$2
            shift;;    
        -I|--image)
            BASE_IMAGE=$2
            shift;;    
        --)
            ;;
        *)
            if [ -z $1 ]; then
                break
            else
                echo "$1 is not a valid option"
                exit 1
            fi;;
    esac
    shift
done

if [ ! -d $BASE_DIR ]; then
    echo "Warning : $BASE_DIR doesn't exist. Creating it..."
    mkdir $BASE_DIR
fi

# Test if the container already exists
echo "Testing existence of $BASE_CT container..."
lxc info $BASE_CT
if [ $? -eq 0 ]; then
    echo "Error : $BASE_CT already exists. Aborting..."
    exit 1
fi
echo "==> OK, $BASE_CT doesn't exist."

# Create the container
lxc launch $BASE_IMAGE $BASE_CT
lxc config set $BASE_CT limits.cpu $BASE_CPU
lxc config set $BASE_CT limits.memory $BASE_MEMORY
lxc config set $BASE_CT boot.autostart true

# Configure the container, depending of OS type
case $BASE_IMAGE in
    "images:ubuntu/artful/amd64"|"ubuntu:artful/amd64"|"images:ubuntu/bionic/amd64")
        # Configure network
        lxc exec ${BASE_CT} -- sh -c "rm /etc/netplan/*.yaml"
        lxc file push ${BASE_DIR}/netplan_config.yaml ${BASE_CT}/etc/netplan/config.yaml
        lxc exec ${BASE_CT} -- sed -i s,%%ETHINT%%,${ETHINT}, /etc/netplan/config.yaml
        lxc exec ${BASE_CT} -- sed -i s,%%ETHEXT%%,${ETHEXT}, /etc/netplan/config.yaml
        lxc exec ${BASE_CT} -- sed -i s,%%GATEWAY%%,${GATEWAY},g /etc/netplan/config.yaml
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_ETHEXT%%/${DNS_ETHEXT}/ /etc/netplan/config.yaml
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_ETHINT%%/${DNS_ETHINT}/ /etc/netplan/config.yaml
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_DOMAINEXT%%/${DNS_DOMAINEXT}/ /etc/netplan/config.yaml
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_DOMAININT%%/${DNS_DOMAININT}/ /etc/netplan/config.yaml
        # Configure logs
        lxc file push ${BASE_DIR}/rsyslog/rsyslog.conf ${BASE_CT}/etc/
        lxc file push ${BASE_DIR}/rsyslog/50-default.conf ${BASE_CT}/etc/rsyslog.d/
        lxc file push ${BASE_DIR}/logrotate/logrotate.conf ${BASE_CT}/etc/
        lxc file push ${BASE_DIR}/logrotate/rsyslog ${BASE_CT}/etc/logrotate.d/
        lxc exec ${BASE_CT} -- sed -i s,/usr/sbin/logrotate\ /etc/logrotate.conf,/usr/sbin/logrotate\ \-f\ /etc/logrotate.conf, /etc/cron.daily/logrotate
        # Configure TimeZone
        lxc exec $BASE_CT -- timedatectl set-timezone Europe/Paris 
        # Deactive motd
        lxc exec $BASE_CT -- sed -i s/ENABLED=1/ENABLED=0/ /etc/default/motd-news
        lxc exec $BASE_CT -- systemctl disable motd-news.timer
        # Configure systemd-resolved
        lxc file push ${BASE_DIR}/resolved.conf ${BASE_CT}/etc/systemd/
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_ETHEXT%%/${DNS_ETHEXT}/ /etc/systemd/resolved.conf
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_ETHINT%%/${DNS_ETHINT}/ /etc/systemd/resolved.conf
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_DOMAINEXT%%/${DNS_DOMAINEXT}/ /etc/systemd/resolved.conf
        lxc exec ${BASE_CT} -- sed -i s/%%DNS_DOMAININT%%/${DNS_DOMAININT}/ /etc/systemd/resolved.conf;;

    "images:debian/jessie/amd64")
        lxc file push ${BASE_DIR}/interfaces ${BASE_CT}/etc/network/    
        lxc exec ${BASE_CT} -- sed -i s,%%ETHINT%%,${ETHINT}, /etc/network/interfaces
        lxc exec ${BASE_CT} -- sed -i s,%%ETHEXT%%,${ETHEXT}, /etc/network/interfaces
        lxc exec ${BASE_CT} -- sed -i s,%%GATEWAY%%,${GATEWAY}, /etc/network/interfaces
        lxc exec ${BASE_CT} -- sh -c "echo 'search $DNS_DOMAINEXT $DNS_DOMAININT' > /etc/resolv.conf"
        lxc exec ${BASE_CT} -- sh -c "echo 'nameserver $DNS_ETHEXT' >> /etc/resolv.conf"
        lxc exec ${BASE_CT} -- sh -c "echo 'nameserver $DNS_ETHINT' >> /etc/resolv.conf";;
    *)
        echo "Image not autorised!"
        exit 1;;
esac

# Configuration AC
lxc file push $SSL_CA_CERTPATH ${BASE_CT}/etc/ssl/certs/

# Configuration SSH
lxc exec ${BASE_CT} -- mkdir /root/.ssh
lxc file push ${BASE_DIR}/authorized_keys ${BASE_CT}/root/.ssh/authorized_keys

# Configuration .bashrc
lxc file push ${BASE_DIR}/.bashrc ${BASE_CT}/root/.bashrc

# Configuration .vimrc
lxc file push ${BASE_DIR}/.vimrc ${BASE_CT}/root/.vimrc

# Configuration LDAP
cat << EOF > ${BASE_DIR}/ldap.conf
URI         $LDAP_URI
BASE        $LDAP_ROOTDN
TLS_CACERT  $SSL_CA_CERTPATH_CT
TLS_REQCERT demand
SIZELIMIT   1000
TIMELIMIT   10
EOF
lxc file push ${BASE_DIR}/ldap.conf ${BASE_CT}/etc/ldap/

lxc restart $BASE_CT

sleep 2

lxc exec $BASE_CT -- apt update

if [ $BASE_IMAGE == "images:debian/jessie/amd64" ]; then
    lxc exec $BASE_CT -- sh -c "apt install -y vim less rsyslog"
    # Correction de l'erreur systemd :
    # systemd-journal-flush.service loaded failed failed Trigger Flushing of Journal to Persistent Storage
    lxc exec ${BASE_CT} -- sh -c "sed -i s/#Storage=auto/Storage=volatile/ /etc/systemd/journald.conf"
fi

lxc exec $BASE_CT -- sh -c "apt install -y apt-utils bash-completion dnsutils openssh-server htop iftop man-db curl tcpdump mlocate net-tools"
