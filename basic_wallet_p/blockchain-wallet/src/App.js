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
  console.log('PROPS', props)

  // const authenticated = false

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
          <Route exact path='/' component={WelcomeForm}/>
          <Route path='/wallet' component={Wallet}/>
      </div>
  );
}

export default App;
