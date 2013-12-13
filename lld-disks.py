#!/usr/bin/python

import json
import subprocess

# Nasty hack for 2.6 Python.
if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


if __name__ == '__main__':
    output = subprocess.check_output("cat /proc/diskstats | awk '{print $3}' | grep -v 'ram\|loop\|sr'", shell=True)
    data = list()
    for line in output.split("\n"):
        if line:
	        data.append({"{#DEVICE}": line, "{#DEVICENAME}": line.replace("/dev/", "")})

    print(json.dumps({"data": data}, indent=4))
