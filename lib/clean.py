from subprocess import Popen, PIPE

p = Popen("ps aux | grep 'pox' | awk '{print $2}'", stdout=PIPE, shell=True)
p.wait()
procs = (p.communicate()[0]).split('\n')
for pid in procs:
    try:
        pid = int(pid)
        Popen('kill %d' % pid, shell=True).wait()
    except:
        pass
