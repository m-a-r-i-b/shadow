import React from 'react';
import { useState } from 'react';
import logo from './logo.svg';
import './App.css';

const App = () => {
  const [count, setCount] =  useState(0);

    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          Current count : {count}.
        </p>
        <button onClick={()=>{setCount(count+1)}}>Click me</button>
      </div>
    );
}

export default App;
