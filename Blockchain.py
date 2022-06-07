import datetime as _dt
import hashlib as _hashlib
import json as _json

class Blockchain:

    def __init__(self):
        self.chain = list()
        genesis_block = self._create_block(data = "I am the genesis block", proof = 1,previous_hash = "0",index =1)
        self.chain.append(genesis_block)
        print("This is the current length:")
        print(len(self.chain))
        print(self.chain)

    def mine_block(self,data:str) -> dict:
        previous_block = self.get_previous_block()
        print("This is the previous block:")
        print(previous_block)
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(previous_proof=previous_proof,index= index, data = data)
        previous_hash = self._hash(block= previous_block)
        block = self._create_block(data=data,proof=proof, previous_hash=previous_hash,index = index)

        self.chain.append(block)
        return block


    def _hash(self,block:dict)-> str:
        """
        Hash a block and return the cryptographic hash value
        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()

    def _to_digest(self,new_proof: int, previous_proof: int,index:int,data:str) -> bytes:
        to_digest = str(new_proof **2 - previous_proof **2 + index) + data
        return to_digest.encode()


    def _proof_of_work(self,previous_proof: str, index: int, data:str) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            print(new_proof)
            to_digest = self._to_digest(new_proof=new_proof,previous_proof=previous_proof,index = index,data = data)

            hash_value = _hashlib.sha256(to_digest).hexdigest()

            if hash_value[:4] == "0000":
                check_proof = True

            else:
                new_proof = new_proof + 1

        return new_proof



    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def _create_block(self,data:str,proof:int, previous_hash:str,index:int) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash" : previous_hash,

        }

        return block



#Function to validate the chain.
    def _is_chain_valid(self)-> bool:
        current_block = self.chain[0]
        block_index =  current_block.get("index")

        while block_index < len(self.chain):
            next_block = self.chain[block_index]

            if next_block["previous_hash"] != self._hash(current_block):
                return False
                print("Chain is Invalid")
            current_proof = current_block["proof"]
            next_index, next_data, next_proof = next_block["index"], next_block["data"],next_block["proof"]

            hash_value = _hashlib.sha256(self._to_digest(new_proof=next_proof, previous_proof=current_proof, index = next_index, data= next_data)).hexdigest()
            if hash_value[:4] != "0000":
                return False
                print("Chain is Invalid")

            current_block = next_block
            block_index = block_index + 1

        print("The chain is valid!")
        return True




bc = Blockchain()
bc.chain
bc.mine_block("Hello Planet")
bc.mine_block("Hello Planet 2")
bc.mine_block("Hello Planet 3")
print(bc.chain)
print(bc._is_chain_valid())
bc.chain[1]["data"] = "Hello MArs"
print(bc._is_chain_valid())
print(bc.chain)