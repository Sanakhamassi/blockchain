# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 18:03:10 2023

@author: sanak
"""

import datetime 
import hashlib 
import json 
from flask import Flask,jsonify 

#building the blockchain  
class Blockhain: 
    def __init__(self): 
        self.chain= [] 
        #the genisses block is the first block of the chain 
        self.createBlock(proof=1,prevHash='0') 
        
    def createBlock(self, proof,prevHash):
        block={"index":len(self.chain )+1,
               "timestamp":str(datetime.datetime.now()),
               "proof":proof, #hash
               "prevHash":prevHash} 
        self.chain.append(block) 
        return block 
    
    def getPrevBlock(self):
        return self.chain[-1]
    
    #problem where minners needs to solve to find the proof of work 
    #the proof is hard to find but easy to verify  
    def proof_of_work(self,prevProof): 
        new_proof = 1 
        check_proof= False  
        while check_proof is False: 
            #the pb that the mnners needs to solve 
            hash_operation=hashlib.sha256(str(new_proof**2-prevProof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof=True 
            else: 
                new_proof+=1 
        return new_proof 
    def hash(self,block):
        #convert a dict to a string
        encoded_block=json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(encoded_block).hexdigest()
    
    def verify_chain(self,chain):
        prev_block=chain[0]
        block_index=1
        while block_index <len(chain): 
            block=chain[block_index]
            if block['prevHash']!=self.hash(prev_block):
                return False 
            prev_proof=prev_block['proof'] 
            current_proof=block['proof'] 
            hash_operation=hashlib.sha256(str(current_proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            prev_block=block
            block_index+=1 
        return True
                
        
app=Flask(__name__) 
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockchain= Blockhain()  
@app.route('/mine_block',methods=['GET']) 
def mine_block():  
    #first we determine the proof of work problem
    prev_block=blockchain.getPrevBlock()
    prev_proof=prev_block['proof'] 
    proof=blockchain.proof_of_work(prev_proof)
    #second cretee the block
    prev_hash=blockchain.hash(prev_block) 
    block=blockchain.createBlock(proof, prev_hash)
    response={ 'message':'congrats, success',
              'index':block['index'],
              'proof':block['proof'],
              'timestamp': block['timestamp'],
              'prev_hash':block['prevHash']} 
    return jsonify(response),200 

@app.route('/chain',methods=['GET']) 
def get_chain():
    response= {'chain':blockchain.chain,
               'length':len(blockchain.chain)}
    return jsonify(response),200 
app.run(host='0.0.0.0',port=5000)

        
        