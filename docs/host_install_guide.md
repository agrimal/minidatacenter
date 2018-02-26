# The MiniDataCenter Project
## Host Install Guide

Description
===========

This guide will show you, from the beginning and step by step, how to configure
your server to be ready to host LXD containers.

We will install Ubuntu 17.10 on a mirrored ZFS volume (equivalent to RAID1) for
a better availability of the system : with 2 disks, one can break and the system
continue running on the other one.

Warning : mirrored ZFS or RAID1 does not dispend you from backuping your data in
a safe place !

Hardware specifications
=======================

First i will tell you about my hardware configuration, so if you're going to buy
the hardware soon, maybe it'll give you some idea. Keep in mind that and old
server or a home computer is just fine to install The Minidatacenter project.

- CPU : Intel Xeon E3 1240v6 (4c/8t) @3,7/3,9 GHz
- Motherboard : ASUS P10S-I (Mini-ITX form-factor)
- RAM : 2 x 16 GB DDR4-2400 MHz ECC Crucial very low profile
- SSD 1 : 240 GB Sandisk Ultra II
- SSD 2 : 240 GB Transcend 220S
- Case : Bitfenix Phenom ITX Black
- Power Supply : Seasonic 550W Platinum

All of these components fit in a small form-factor (ITX), while their
performance is still impressive for a home user.
The plus here is an IPMI interface on the motherboard, allowing you to take
control of the server over the network.
All the containers are stored directly on the mirrored SSD's.
ECC memory allow for more stable platform, even this this not really necessary
at home.

I recommend using at least a dual-core CPU with SMT / Hyperthreading or a quad-
core without it.
For the RAM my recommands are at least 8 GB because we are using zfs here and
zfs is effective at the cost of high memory consumption.

First steps
===========

Make a bootable USB key with the Ubuntu 17.10 live-CD.
You can download the ISO on the [Ubuntu website](https://www.ubuntu.com/download/alternative-downloads)
Choose the desktop version because we need the live-CD.

1. Boot the live-CD.

2. Open a terminal and edit your source list `/etc/apt/sources.list.d/base.list`.

Clear everything and add the following lines :
```
deb http://deb.debian.org/debian stretch main contrib non-free
deb http://deb.debian.org/debian stretch-updates main contrib non-free
deb http://security.debian.org/ stretch/updates main contrib non-free
```

3. Update all the packages :
```bash
apt update && apt -y upgrade
```

4. From now you can install an ssh server and maybe your favorite text editor :
```bash
apt install openssh-server vim
```

5. If you want to connect to your server as root, edit the file
`/etc/ssh/sshd_config` and add the following line :
```
PermitRootLogin yes
```

6. Restart the ssh daemon :
```bash
systemctl restart ssh.service
```
Now you can connect to your server via SSH.

7. Install the following packages :
```bash
apt install debootstrap gdisk linux-headers-$(uname -r) zfs-dkms
```

8. Load the zfs module :
```bash
modprobe zfs
```

9. Identify your hard drives and store their path in variables :
```bash
ls -l /dev/disk/by-id/
```
For example mine are :
```
/dev/disk/by-id/ata-SanDisk_Ultra_II_240GB_171028800778
/dev/disk/by-id/ata-TS240GSSD220S_032272B0D88187210048
```
So I use these commands :
```bash
FIRST_DISK='/dev/disk/by-id/ata-SanDisk_Ultra_II_240GB_171028800778'
SECOND_DISK='/dev/disk/by-id/ata-TS240GSSD220S_032272B0D88187210048'
```

10. Create the GPT partitions :
```bash
sgdisk -n3:1M:+512M -t3:EF00 $FIRST_DISK 
sgdisk -n1:0:0 -t1:BF01 $FIRST_DISK
sgdisk -n3:1M:+512M -t3:EF00 $SECOND_DISK
sgdisk -n1:0:0 -t1:BF01 $SECOND_DISK
```

11. Configure the zfs pool :
```bash
zpool create -f -o ashift=12 -O atime=off -O canmount=off -O compression=lz4 \
    -O normalization=formD -O mountpoint=/ -R /mnt rpool mirror \
    ${FIRST_DISK}-part1 ${SECOND_DISK}-part1
```

12. Create the zfs datasets :
```bash
zfs create -o canmount=off -o mountpoint=none rpool/ROOT
zfs create -o canmount=noauto -o mountpoint=/ rpool/ROOT/debian
zfs mount rpool/ROOT/debian
zpool set bootfs=rpool/ROOT/debian rpool
zfs create -o setuid=off rpool/home
zfs create -o mountpoint=/root rpool/root
zfs create -o canmount=off -o setuid=off -o exec=off rpool/var
zfs create -o com.sun:auto-snapshot=false rpool/var/cache
zfs create rpool/var/log
zfs create rpool/var/spool
zfs create -o com.sun:auto-snapshot=false -o exec=on rpool/var/tmp
zfs create rpool/srv
```
-- to be continued
