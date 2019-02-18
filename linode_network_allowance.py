#!/usr/bin/python3

# Use the official linode api module,
# https://github.com/linode/linode_api4-python
# pip3 install linode_api4

import linode_api4,sys,os,argparse

# Make sure to export an API token from the
# cloud site, not your "profile" as the older
# documentation will suggest.
# https://cloud.linode.com/profile/tokens
# https://developers.linode.com/api/v4#section/Introduction

parser = argparse.ArgumentParser(description="Check Linode data usage.")
parser.add_argument("-w",metavar="WARN",type=str,required=True,help="Warning threshold in gigabytes or %%")
parser.add_argument("-c",metavar="CRIT",type=str,required=True,help="Critical threshold in gigabytes or %%")
parser.add_argument("-k",metavar="KEY",type=str,help="Linode API Key.")
parser.add_argument("-f",metavar="KEYFILE",type=str,help="Linode API Key in plaintext file.")
parser.add_argument("-i",action="store_true",help="Show quota free instead of used.")
args = parser.parse_args()

if args.w[-1] == '%' and args.c[-1] == '%':
    metric = "percent"
    warn = int(args.w[:-1])
    crit = int(args.c[:-1])
elif args.w[-1] == '%' or args.c[-1] == '%':
    print("Type mismatch for crit/warn. Please use percent or gigabyte values.")
    sys.exit(3)
else:
    metric = "gigabytes"
    warn = int(args.w)
    crit = int(args.c)

if args.k:
    key = args.k
elif args.f:
    with open(args.f,'r') as f:
        key = f.read().strip()
else:
    print("UNKNOWN: No api key specified.")
    sys.exit(3)

try:
    lin = linode_api4.LinodeClient(key)
except Exception as e:
    print(f"UNKNOWN: problem with API key. Error: {e}")
    sys.exit(3)

transfer = lin.account.transfer()
quota = transfer.quota
used = transfer.used
free = quota - used
billable = transfer.billable

percused = (used / quota) * 100
percfree = 100 - percused

if args.i:
    perfdata = f'free_perc={percfree};;;0;100 free_gig={free};;;0;{quota}'
    output = f'{percfree:.2f}% of quota free. Free: {free}GB Total: {quota}GB|{perfdata}'
    warn = 100 - warn
    crit = 100 - crit
else:
    perfdata = f'used_perc={percused};;;0;100 used_gig={used};;;0;{quota}'
    output = f'{percused:.2f}% of quota used. Used: {used}GB Total: {quota}GB|{perfdata}'    
    
if billable > 0:
    print(f"CRITICAL: Quota breached, {billable}GB currently billable!|{perfdata}")
    sys.exit(2)

if metric == 'percent':
    compareval = percused
else:
    compareval = used
    
if compareval >= crit:
    print(f"CRITICAL: {output}")
    sys.exit(2)
elif compareval >= warn:
    print(f"WARNING: {percused:.2f}% of quota used. [{used}GB / {quota}GB]|{perfdata}")
    sys.exit(1)
else:
    print(f"OK: {percused:.2f}% of quota used. [{used}GB / {quota}GB]|{perfdata}")
    sys.exit(0)
