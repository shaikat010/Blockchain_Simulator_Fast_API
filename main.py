import fastapi as _fastapi
import Blockchain as _blockchain

blockchain = _blockchain.Blockchain()

app = _fastapi.FastAPI()


#endpoint to mine a block
@app.post("/mine_block")
def mine_block(data:str):
    if not blockchain._is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid!")

    block = blockchain.mine_block(data= data)

    return block

#endpoint to return the entire blockchain
@app.get("/blockchain/")
def get_blockchain():
    if not blockchain._is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid!")

    chain = blockchain.chain
    return chain


# endpoint that returns the previous block
@app.get("/previous_block/")
def previous_block():
    if not blockchain._is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid!")

    return blockchain.get_previous_block()



#endpoint to see if the blockchain is valid
@app.get("/validate/")
def is_blockchain_valid():
    return blockchain._is_chain_valid()

