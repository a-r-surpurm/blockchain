from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib
import json
import base64

class AESCTRCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        nonce = os.urandom(16)  
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(nonce), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return base64.b64encode(nonce + ciphertext).decode()

    def decrypt(self, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        nonce, ciphertext = encrypted_data[:16], encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CTR(nonce), backend=default_backend())
        decryptor = cipher.decryptor()
        
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode()

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), transactions, previous_hash)
        self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i - 1].hash:
                return False
        return True


key = os.urandom(32)


cipher = AESCTRCipher(key)

transaction_data = "Alice pays Bob 10 BTC"
encrypted_transaction = cipher.encrypt(transaction_data)
blockchain = Blockchain()
blockchain.add_block(encrypted_transaction)
decrypted_transaction = cipher.decrypt(blockchain.chain[1].transactions)
print("Original Transaction:", transaction_data)
print("Encrypted Transaction:", blockchain.chain[1].transactions)
print("Decrypted Transaction:", decrypted_transaction)
print("Blockchain Valid:", blockchain.verify_chain())
