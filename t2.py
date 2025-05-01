import psutil
import subprocess
import signal

from util import wait_for_signal

print(psutil.Process().pid)
for flavor in ("baseline", "json", "orjson", "dataclass", "pydantic"):
    proc = subprocess.Popen(("python", "t.py",flavor), stdin=subprocess.PIPE)
    wait_for_signal(signal.SIGUSR1)

    psutil_proc = psutil.Process(proc.pid)
    rss = psutil_proc.memory_info().rss

    print(f"{flavor}: {round(rss/1024/1024, 2)} MB")
    proc.send_signal(signal.SIGUSR2)

    proc.wait()
    print()



proc = subprocess.Popen(("./t"), stdin=subprocess.PIPE)
for flavor in ("go raw", "go struct"):
    wait_for_signal(signal.SIGUSR1)

    psutil_proc = psutil.Process(proc.pid)
    rss = psutil_proc.memory_info().rss

    print(f"{flavor}: {round(rss/1024/1024, 2)} MB")
    proc.send_signal(signal.SIGUSR2)

proc.wait()
print()
