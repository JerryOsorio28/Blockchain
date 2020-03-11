import React from 'react'

const Wallet = props => {

    console.log('props from wallet', props)

    return (
        <div>{`Welcome to your wallet ${props.user.username}!`}</div>
    )
}

export default Wallet