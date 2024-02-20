import './App.css';
import Login from './login';
import p2 from './p2.png'
import { useState } from 'react';
import Preprocess from './preprocess';

function App() {
  const [loggedIn, setLoggedIn]=useState(false);
  return (
    <div className="App">
      <div className=''>
        <img src={p2} alt="" height="150px"/>
        {!loggedIn && <Login loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>}
        {loggedIn && <Preprocess />}
      </div>
    </div>
  );
}

export default App;
