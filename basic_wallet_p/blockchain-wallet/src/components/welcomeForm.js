import React, { useState } from 'react';

const WelcomeForm = props => {
    const [user, SetUser] = useState({
        username: '',
        valid: false,
        errorMessage: ''
    })

    console.log('state', user)
    console.log('props', props)

    const userHandler = e => {
        // console.log('input', e.target.name)
        const input = {...user, [e.target.name]: e.target.value}
        SetUser(input)
    }

    const submitHandler = e => {
        e.preventDefault()
        if(user.username === ''){
            SetUser({...user, errorMessage: <p style={{color: 'red', fontWeight: 'bold'}}>*You must type and username to continue.</p>})
        }
        else if(user.username.length < 4){
            SetUser({...user, errorMessage: <p style={{color: 'red', fontWeight: 'bold'}}>*Username must be at least 4 characters long.</p>})
        } else {
            SetUser({...user, valid: true})
            props.history.push('/wallet')
        }
    }

    return (
        <>
            <h1>Thank you for testing our Wallet App!</h1>
            <h3>What would you like your username to be?</h3>
            {user.valid === false ? 
                <div>{user.errorMessage}</div>
            : null}
            <form>
                <input 
                    placeholder='Username'
                    name='username'
                    value={user.username}
                    onChange={userHandler}
                    style={{marginTop: '10px'}}
                >
                </input>
                <button to='/wallet' onClick={submitHandler} >Let's Go!</button>
            </form>
        </>
    )
}

export default WelcomeForm