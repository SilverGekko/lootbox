import rsa

pubkeyname = 'public.pem'
privkeyname = 'private.pem'

pubkey, privkey = rsa.newkeys(4096)

with open(pubkeyname, mode='wb') as publicfile:
    publicfile.write(rsa.PublicKey.save_pkcs1(pubkey))

with open(privkeyname, mode='wb') as privatefile:
    privatefile.write(rsa.PrivateKey.save_pkcs1(privkey))