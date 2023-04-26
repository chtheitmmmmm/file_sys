from Crypto.Cipher import DES
import binascii


# 这是密钥
key = b'abcdefgh'   # key需为8字节长度.
# 需要去生成一个DES对象
des = DES.new(key, DES.MODE_ECB)
# 需要加密的数据
text = 'python spider!'     # 被加密的数据需要为8字节的倍数.
text = text + (8 - (len(text) % 8)) * '='
print(text)
# 加密的过程
encrypto_text = des.encrypt(text.encode())
# encrypto_text = binascii.b2a_hex(encrypto_text)
print(encrypto_text)

decrrpto_text = des.decrypt(encrypto_text)
# decrrpto_text = binascii.b2a_hex(decrrpto_text)
print(decrrpto_text)