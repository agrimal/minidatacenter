#!/usr/bin/env python3

import colorama, re, math, subprocess as sp, platform, sys, psutil, os
from colorama import Fore, Style

# Convert int (B) to str (GB) with 2 decimals
def convert_mem(value):
    return str( round(value / math.pow(1024, 3), 2))

# Convert float to str with 1 decimal
def convert_mem_percent(value):
    return str( round(value, 1))

# 1) uptime
with open('/proc/uptime', 'r') as proc_uptime:
    uptime_seconds = float(proc_uptime.readline().split()[0])
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    del seconds
    days = int(days)
    hours = int(hours)
    minutes = int(minutes)
    uptime = ' '.join((str(days), "days", str(hours), "hours", str(minutes), 
        "minutes"))

# 2) distrib
distrib = ' '.join(platform.linux_distribution())

# 3) kernel
kernel = platform.uname().release

# 4) mem
mem_total        = convert_mem(psutil.virtual_memory().total)
mem_used         = convert_mem(psutil.virtual_memory().used)
mem_percent      = convert_mem_percent(psutil.virtual_memory().percent)
mem_buffer_cache = convert_mem(psutil.virtual_memory().buffers + 
    psutil.virtual_memory().cached)
mem_avail        = convert_mem(psutil.virtual_memory().available)

mem = "Used: " + mem_used + "/" + mem_total + " GB (" + mem_percent + \
    "%) | Buffers/Cached: " + mem_buffer_cache + " GB | Avail.: " + mem_avail + \
    " GB"

# 5) swap
swap_total   = convert_mem(psutil.swap_memory().total)
swap_used    = convert_mem(psutil.swap_memory().used)
swap_percent = convert_mem_percent(psutil.swap_memory().percent)
swap = "Used: " + swap_used + "/" + swap_total + " GB (" + swap_percent + "%)"

# 6) cpu
with sp.Popen("lscpu", stdout=sp.PIPE) as p:
    regexp = r'^.+?[ \t]*:[ \t]*(.+?)$'
    for line in p.stdout.readlines():
        line = line.decode('utf-8').rstrip()
        if "Model name" in line:
            cpu_model = re.sub(regexp, r'\1', line)
        if "Socket(s)" in line:
            cpu_number = re.sub(regexp, r'\1', line)
        if "Core(s) per socket" in line:
            cpu_core_per_socket = re.sub(regexp, r'\1', line) 
        if "Thread(s) per core" in line:
            cpu_thread_per_core = re.sub(regexp, r'\1', line)
cpu_thread_number_per_socket = int(cpu_core_per_socket) * int(cpu_thread_per_core)
cpu = cpu_number + " x " + cpu_model + " (" + cpu_core_per_socket + "c/" + \
    str(cpu_thread_number_per_socket) + "t)"

# 7) load
load = str(round(os.getloadavg()[0], 2)) + " " + \
    str(round(os.getloadavg()[1], 2)) + " " + str(round(os.getloadavg()[2], 2))

# 8) zpool_header, zpool_list
zpool_list = []
with sp.Popen("zpool list -o name,size,alloc,free,fragmentation,capacity," + 
    "dedupratio", stdout=sp.PIPE, shell=True) as p:
    i = 0
    for line in p.stdout.readlines():
        line = line.decode('utf-8').rstrip()
        if i == 0:
            zpool_header = line
        else:
            zpool_list.append(line)
        i = i + 1

# 9) zfs_header, zfs_list
zfs_list = []                                                                  
with sp.Popen("zfs list -o name,used,usedsnap,avail,mountpoint -d 2",
    stdout=sp.PIPE, shell=True) as p:
    i = 0                                                                        
    for line in p.stdout.readlines():                                            
        line = line.decode('utf-8').rstrip()                                     
        if i == 0:                                                               
            zfs_header = line                                                  
        else:                                                                    
            zfs_list.append(line)                                              
        i = i + 1

# 10) ip_list
ip_list = []
with sp.Popen("ip -family inet -oneline address show", stdout=sp.PIPE, shell=True) as p:
    re_ip = re.compile(r"^[0-9]+: ([\w-]+)[ \t]+inet ([0-9\./]+).*$")
    for line in p.stdout.readlines():
        line = line.decode('utf-8').rstrip()
        m = re_ip.search(line)
        ip_list.append(m.groups()[0] + ": " + m.groups()[1])

# 11) hostname
hostname = platform.node()


colorama.init()

output = []
default_prefix_color = Fore.YELLOW
default_string_color = Fore.RESET

output.append({ 'prefix' : 'Hostname : ', 'string' : hostname })
output.append({ 'prefix' : 'Distrib. : ', 'string' : distrib })
output.append({ 'prefix' : 'Kernel   : ', 'string' : kernel })
output.append({ 'prefix' : 'Uptime   : ', 'string' : uptime })
output.append({ 'prefix' : 'CPU      : ', 'string' : cpu })
output.append({ 'prefix' : 'Load     : ', 'string' : load })
output.append({ 'prefix' : 'Memory   : ', 'string' : mem })
output.append({ 'prefix' : 'Swap     : ', 'string' : swap })
output.append({ 'prefix' : '', 'string' : '' })
output.append({ 'prefix' : 'Disk usage :', 'string' : '' })
output.append({ 'prefix' : '', 'string' : '' })
output.append({ 'prefix' : '    ZFS Pools', 'string' : '',
    'prefix_color' : Fore.GREEN })
output.append({ 'prefix' : '    ', 'string' : zpool_header,
    'string_color' : Fore.RESET + Style.BRIGHT })
for line in zpool_list:
    output.append({ 'prefix' : '    ', 'string' : line })
output.append({ 'prefix' : '', 'string' : '' })
output.append({ 'prefix' : '    ZFS Datasets', 'string' : '',
    'prefix_color' : Fore.GREEN })
output.append({ 'prefix' : '    ', 'string' : zfs_header,
    'string_color' : Fore.RESET + Style.BRIGHT })
for line in zfs_list:
    output.append({ 'prefix' : '    ', 'string' : line })
output.append({ 'prefix' : '', 'string' : '' })
output.append({ 'prefix' : 'IP addresses :', 'string' : '' })
output.append({ 'prefix' : '', 'string' : '' })
for line in ip_list:
    output.append({ 'prefix' : '    ', 'string' : line })

max_len = max( len(line['prefix'] + line['string']) for line in output )

print(Fore.BLUE + '┏' + '━' * (max_len + 4) + '┓')
print('┃┏' + '━' * (max_len + 2) + '┓┃')
for line in output:
    print(Fore.BLUE + '┃┃ ', end='')
    print(line['prefix_color'] if 'prefix_color' in line else 
        default_prefix_color, end='')
    print(line['prefix'], end='')
    print(line['string_color'] if 'string_color' in line else           
        default_string_color, end='')
    print(line['string'], end='')
    print(' ' * (max_len - len(line['prefix'] + line['string']) + 1) +
        Style.RESET_ALL + Fore.BLUE + '┃┃')
print(Fore.BLUE + '┃┗' + '━' * (max_len + 2) + '┛┃')
print('┗' + '━' * (max_len + 4) + '┛' + Style.RESET_ALL)

colorama.deinit()
