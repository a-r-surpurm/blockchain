import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.incentive_ledger = {}  # Stores e-cash balances

        # Create the Genesis Block
        self.create_block(patient_id="GENESIS", doctor_id="SYSTEM", action="Genesis Block")

    def create_block(self, patient_id, doctor_id, action, test_results=None, prescription=None):
        prev_hash = self.chain[-1]['hash'] if self.chain else '0'
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'action': action,
            'test_results': test_results,
            'prescription': prescription,
            'previous_hash': prev_hash,
        }
        block['hash'] = self.hash_block(block)
        self.chain.append(block)

        # Incentive system
        if doctor_id != "SYSTEM":
            self.update_incentive(doctor_id, 10)  # Give 10 e-cash per action

        return block

    def update_incentive(self, entity, amount):
        if entity not in self.incentive_ledger:
            self.incentive_ledger[entity] = 0
        self.incentive_ledger[entity] += amount

    def get_incentives(self):
        return self.incentive_ledger

    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_last_block(self):
        return self.chain[-1] if self.chain else None
