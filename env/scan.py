from scapy.all import *


def syn_scan(dst: str, src=None, dport=80):
    # get = 'GET / HTTP/1.0\n\n'

    ip = IP(src=src, dst=dst)

    port = RandNum(1024,65535)

    SYN = ip/TCP(sport=port, dport=dport, flags="S")

    SYNACK = sr1(SYN)
    print(SYNACK.sprintf("%IP.src%;%TCP.sport%;%TCP.flags%"))


if __name__ == "__main__":
    syn_scan(dst="172.29.130.7", dport=22)
