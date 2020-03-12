import React from 'react'

const Wallet = props => {

    const proofOfWork = block => {
        let blockString = JSON.stringify(block)
        let proof = 0

        while(validProof(blockString, proof) === false){
            proof++
        }
        return proof
    }

    const validProof = (blockString, proof) => {
        let guess = encodeURI(`${blockString}${proof}`)
        let guess_hash = hashlib.sha256(guess).hexdigest
    }

    return (
        <div>{`Welcome to your wallet ${props.user.username}!`}</div>
    )
}

export default Wallet