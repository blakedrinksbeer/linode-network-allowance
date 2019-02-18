# Linode Network Allowance Monitor

This will query Linode's API for how much of your network transfer pool is available, and output perfdata showing the percentage and total gigabytes used.

Requirements:
* Python 3.6+
* linode_api4

```
usage: linode_network_allowance.py [-h] -w WARN -c CRIT [-k KEY] [-f KEYFILE]
                                   [-i]

Check Linode data usage.

optional arguments:
  -h, --help  show this help message and exit
  -w WARN     Warning threshold in gigabytes or %
  -c CRIT     Critical threshold in gigabytes or %
  -k KEY      Linode API Key.
  -f KEYFILE  Linode API Key in plaintext file.
  -i          Show quota free instead of used.
```

Linode's API module is available on github.
* https://github.com/linode/linode_api4-python

I just use pip:
```
pip3 install linode_api4
```

Create an access token:
* https://cloud.linode.com/profile/tokens

And lastly, browse the API documentation here:
* https://developers.linode.com/api/v4#section/Introduction