from src.recon_checkip import CheckIP

c=CheckIP()
r=c._get_ip_by_host_dns('124.89.116.178')
print(r)