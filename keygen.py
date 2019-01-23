import rsa
import os
pid = os.getpid()
length=4096
pubkeyname = 'public%d.pem' % pid
privkeyname = 'private%d.pem' % pid

pubkey, privkey = rsa.newkeys(length)

with open(pubkeyname, mode='wb') as publicfile:
    publicfile.write(rsa.PublicKey.save_pkcs1(pubkey))

with open(privkeyname, mode='wb') as privatefile:
    privatefile.write(rsa.PrivateKey.save_pkcs1(privkey))