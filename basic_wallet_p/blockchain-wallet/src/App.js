import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import WelcomeForm from './components/welcomeForm';
import {Route} from 'react-router-dom';
import Wallet from './components/wallet'


function App(props) {

  const [chain, setChain] = useState()
  console.log('Entire Blockchain', chain)

  const [user, setUser] = useState({
    username: '',
    valid: false,
    errorMessage: ''
})

console.log('User from App', user)

  useEffect(() => {
    axios.get('http://localhost:5000/chain')
    .then(res => {
      // console.log(res.data.chain)
      let chain = res.data.chain
      setChain(chain)

    })
    .catch(err => {
      console.log(err.response)
    })
  }, [])


  return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1>Blockchain Wallet</h1>
        </header>
          <Route 
            exact path='/'
            render={props => <WelcomeForm {...props} user={user} setUser={setUser} />}
          />
          <Route 
            path='/wallet'
            render={props => <Wallet {...props} user={user} setUser={setUser} />}
          />
      </div>
  );
}

export default App;
