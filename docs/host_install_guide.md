# The MiniDataCenter Project
## Host Install Guide

Description
===========

This guide will show you, from the beginning and step by step, how to configure  
your server to be ready to host LXD containers.

We will install Ubuntu 18.04 on a mirrored ZFS volume (equivalent to RAID1) for  
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
performance is still impressive for a home usage.  
The plus here is an IPMI interface on the motherboard, allowing you to take  
control of the server over the network, and load ISO images from a remote  
computer.
All the containers are stored directly on the mirrored SSD's.  
ECC memory allow for more stable platform, but this this not really necessary  
at home.

I recommend using at least a dual-core CPU with SMT / Hyperthreading or a quad-  
core without it.  
Concerning the memory, I recommend at least 8 GB because we are using zfs here  
and zfs increases performance at the cost of high memory consumption.

Prerequisites
=============

This tutorial suppose you already have a DHCP and a DNS in your network.  
The Gateway, also serving as a DNS/DHCP server, has address 192.168.1.1.  
Replace it with yours when needed.

First steps
===========

Make a bootable USB key with the Ubuntu 18.04 ISO, or load it with your IPMI  
interface.  
You can download the ISO on the
[Ubuntu website](http://cdimage.ubuntu.com/daily-live/current/HEADER.html).  
Choose the desktop version because we need the live-CD functionality.

1. Boot the Ubuntu 18.04 ISO and choose `Try ubuntu without installing`.

2. Once you're on the desktop, open a terminal and change to root user.
```bash
sudo su
```

3. Install an ssh server and your favorite text editor.
```bash
apt update
apt install --yes vim openssh-server
```

4. Add a password to the root user. Choose something simple as it's just temporary.
```bash
passwd
```

5. Edit the openssh server configuration file `/etc/ssh/sshd_config` and add the  
following line :
```
PermitRootLogin yes
```

6. Restart the ssh daemon :
```bash
systemctl reload ssh
```
Now you can connect to your server via SSH from your computer, so you can copy /
paste the next commands.  
(You can see your IP address with `ip a`)

7. Change repositories
```bash
cat << EOF > /etc/apt/sources.list
deb http://archive.ubuntu.com/ubuntu/ bionic main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted universe multiverse
EOF
```

8. Install packages
```bash
apt update
apt install --yes debootstrap zfs-dkms
```
Read the warning about ZFS and Linux licenses incompatibility and press "OK".  
Building the ZFS kernel module can take several minutes, be patient.

9. Load the ZFS module
```bash
modprobe zfs
```

10. Identify your hard drives and store their path in variables :
```bash
ls -l /dev/disk/by-id/
```
For example mines are :
```
/dev/disk/by-id/ata-SanDisk_Ultra_II_240GB_171028800778
/dev/disk/by-id/ata-TS240GSSD220S_032272B0D88187210048
```
So I use these commands :
```bash
FIRST_DISK='/dev/disk/by-id/ata-SanDisk_Ultra_II_240GB_171028800778'
SECOND_DISK='/dev/disk/by-id/ata-TS240GSSD220S_032272B0D88187210048'
```

11. Create the GPT partitions :
If there was something installed on the disks before, delete the old partitions.
```bash
sgdisk --zap-all $FIRST_DISK
sgdisk --zap-all $SECOND_DISK
```
Then create the new partitions.
```bash
sgdisk -n3:1M:+512M -t3:EF00 $FIRST_DISK 
sgdisk -n1:0:0 -t1:BF01 $FIRST_DISK
sgdisk -n3:1M:+512M -t3:EF00 $SECOND_DISK
sgdisk -n1:0:0 -t1:BF01 $SECOND_DISK
```
If a ZFS pool was configured before, run the following commands :
```bash
zpool import -f rpool
zpool destroy rpool
```

13. Configure the mirrored ZFS pool `rpool` on the 2 hard drives :
```bash
zpool create -f -o ashift=12 -O atime=off -O canmount=off -O compression=lz4 \
    -O normalization=formD -O mountpoint=/ -R /mnt rpool mirror \
    ${FIRST_DISK}-part1 ${SECOND_DISK}-part1
```

14. Create the zfs datasets :
```bash
zfs create -o canmount=off -o mountpoint=none rpool/ROOT
zfs create -o canmount=noauto -o mountpoint=/ rpool/ROOT/ubuntu
zfs mount rpool/ROOT/ubuntu
zpool set bootfs=rpool/ROOT/ubuntu rpool
zfs create -o setuid=off rpool/home
zfs create -o mountpoint=/root rpool/root
zfs create -o canmount=off -o setuid=off -o exec=off rpool/var
zfs create -o com.sun:auto-snapshot=false rpool/var/cache
zfs create rpool/var/log
zfs create rpool/var/spool
zfs create -o com.sun:auto-snapshot=false -o exec=on rpool/var/tmp
zfs create rpool/srv
zfs create -V 10G -b $(getconf PAGESIZE) -o compression=zle -o logbias=throughput -o sync=always -o \
    primarycache=metadata -o secondarycache=none -o com.sun:auto-snapshot=false rpool/swap
```

15. Change permissions on `/mnt/var/tmp`
```bash
chmod 1777 /mnt/var/tmp
```

16. Install Ubuntu 18.04
```bash
debootstrap bionic /mnt
```

17. Configure the hostname of your server
```bash
MYSERVERNAME="mynewserver"
echo $MYSERVERNAME > /mnt/etc/hostname
echo -e "127.0.0.1\tlocalhost\n127.0.1.1\t$MYSERVERNAME" > /mnt/etc/hosts
```

18. Configure repositories
```bash
cat << EOF > /mnt/etc/apt/sources.list
deb http://archive.ubuntu.com/ubuntu/ bionic main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted universe multiverse
EOF
```

19. Configure the network
In this example my server has 2 network interfaces and i leave them in DHCP.
The server will get a static IP address later.
Just make sure with the `ip a` command that your main interface name is 'eno1'.
If you don't know how to configure your network with Netplan, please read the
documentation [here](http://manpages.ubuntu.com/manpages/artful/man5/netplan.5.html)
```bash
cat << EOF > /mnt/etc/netplan/config.yaml
network:
    ethernets:
        eno1:
            dhcp4: yes
            dhcp6: no
        eno2:
            dhcp4: no
            dhcp6: no
EOF
```

20. Prepare the chroot
```bash
mount --rbind /dev /mnt/dev
mount --rbind /proc /mnt/proc
mount --rbind /sys /mnt/sys
```

21. Chroot into the /mnt directory
```bash
chroot /mnt /bin/bash --login
```

22. Give a password to root
```bash
passwd
```

23. Configure the locale
```bash
locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8
```

24. Install packages
```bash
apt update
apt install --yes --no-install-recommends linux-image-generic
apt install --yes zfs-initramfs dosfstools grub-efi-amd64 openssh-server
```

25. Modify the way /var/log and /var/tmp are mounted
```bash
zfs set mountpoint=legacy rpool/var/log
zfs set mountpoint=legacy rpool/var/tmp

cat >> /etc/fstab << EOF
rpool/var/log /var/log zfs defaults 0 0
rpool/var/tmp /var/tmp zfs defaults 0 0
EOF
```

26. Modify the Grub options
```bash
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT.*/GRUB_CMDLINE_LINUX_DEFAULT="ipv6.disable=1"/' /etc/default/grub
update-grub
```

27. Format and configure the EFI partitions
```bash
FIRST_DISK='/dev/disk/by-id/ata-SanDisk_Ultra_II_240GB_171028800778'
SECOND_DISK='/dev/disk/by-id/ata-TS240GSSD220S_032272B0D88187210048'

mkdosfs -F 32 -n EFI "${FIRST_DISK}-part3"
mkdosfs -F 32 -n EFI "${SECOND_DISK}-part3"

mkdir /boot/efi
mount "${FIRST_DISK}-part3" /boot/efi
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu1 --recheck --no-floppy
umount /boot/efi
mount "${SECOND_DISK}-part3" /boot/efi
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu2 --recheck --no-floppy
```

28. Configure the swap
```bash
mkswap -f /dev/zvol/rpool/swap
echo /dev/zvol/rpool/swap none swap defaults 0 0 >> /etc/fstab
swapon -av
```

29. Deactivate logs compression
You don't need to compress files since compression is done on the filesystem
level with ZFS
```bash
for file in /etc/logrotate.d/* ; do
    if grep -Eq "(^|[^#y])compress" "$file" ; then
        sed -i -r "s/(^|[^#y])(compress)/\1#\2/" "$file"
    fi
done
```

30. Modify the ARC size for ZFS (set limit to memory for ZFS)
You can set for example 2GB minimum : 2147483648 bytes
And 16GB for maximum : 17179869184 bytes
```bash
echo -e "options zfs zfs_arc_min=2147483648\noptions zfs \
zfs_arc_max=17179869184" > /etc/modprobe.d/zfs.conf
```

31. Create new initramfs
```bash
update-initramfs -u -k all
```

32. Allow password login for user root with ssh
You may want to disable this later for security reasons
```bash
sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
```

33. Snapshot your system
```bash
zfs snapshot rpool/ROOT/ubuntu@first_install
```

34. Exit chroot, unmount partitions and reboot
```bash
exit
mount | grep -v zfs | tac | awk '/\/mnt/ {print $3}' | xargs -i{} umount -lf {}
systemctl reboot
```
At this point, your server may hang, just reset it.\
On the first boot, zfs will complain that the "rpool" pool cannot be imported
because it was in used by another system.\
Just force import the pool and reboot again.
```bash
zfs import -f rpool
reboot
```

35. You can now log in your freshly installed Ubuntu 18.04 server and start
installing and configuring LXD.
