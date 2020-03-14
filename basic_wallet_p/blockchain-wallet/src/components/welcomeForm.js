import React from 'react';

const WelcomeForm = props => {

    console.log('props', props)

    const userHandler = e => {
        const input = {...props.user, [e.target.name]: e.target.value}
        props.setUser(input)
    }

    const submitHandler = e => {
        e.preventDefault()
        if(props.user.username === ''){
            props.setUser({...props.user, errorMessage: <p style={{color: 'red', fontWeight: 'bold'}}>*You must type an username to continue.</p>})
        }
        else if(props.user.username.length < 4){
            props.setUser({...props.user, errorMessage: <p style={{color: 'red', fontWeight: 'bold'}}>*Username must be at least 4 characters long.</p>})
        } else {
            props.setUser({...props.user, valid: true})
            props.history.push('/wallet')
        }
    }

    return (
        <>
            <h1>Thank you for testing our Wallet App!</h1>
            <h3>What would you like your username to be?</h3>
            {props.user === undefined ? null : props.user.valid === false ? 
                <div>{props.user.errorMessage}</div>
            : null}
            <form>
                <input 
                    placeholder='Username'
                    name='username'
                    value={props.user === undefined ? null : props.user.username}
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