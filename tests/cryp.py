from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP

data = b'1234556'

h = MD5.new(data)   # 哈希值

key = RSA.generate(1024)    # 密钥

s = pkcs1_15.new(key.public_key())  # 用于验证签名

sig = pkcs1_15.new(key).sign(h)   # 签名

s.verify(h, sig + b'1')
