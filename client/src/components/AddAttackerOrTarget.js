import React, { useState } from 'react';

function AddAttackerOrTarget() {

  const [state, setState] = useState('target');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [resStatus, setresStatus] = useState();

  function onTypeChange(value){
    setState(value);
    setName('');
    setEmail('');
    setPassword('');
    setMessage('');
  }

  function submitAdding(event){
    event.preventDefault();
    const reqOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify( { type: state, name: name, email: email, password: password } )
    };
    fetch('/add_attacker_or_target', reqOptions)
      .then(response => response.json())
      .then(data => {console.log(data); {setMessage(data.message); setresStatus(data.status)}});
  }

  return (
    <div className="add">
      <h3>Add attacker or target</h3>

        <form method = "post" onSubmit={submitAdding}>
            <div className="radio-btn">
                <input type="radio" name="attacker_Target" value="target" checked={state==='target'} onChange={event => onTypeChange(event.target.value)}/> Target
                <input type="radio" name="attacker_Target" value="attacker" checked={state==='attacker'} onChange={event => onTypeChange(event.target.value)}/> Attacker
            </div>
            <div className="inputs">
                <label for = "name">Name</label>
                <input type = "text" name = "name" placeholder = "Name" value={name} onChange={e => setName(e.target.value)}/>
                <label for = "email">Email</label>
                <input type = "text" name = "email" placeholder = "email" value={email} onChange={e => setEmail(e.target.value)}/>
                {state === 'target' ? null :
                <div className="inputs">
                  <label for = "password">password</label>
                  <input type = "text" name = "password" placeholder = "password" value={password} onChange={e => setPassword(e.target.value)}/>
                </div>
                }
                <input type = "submit" value = "Submit"/>
            </div>
        </form>
        <p className='message' style={{color: resStatus === 200 ? 'green' : 'red'}}>{message ? message : null}</p>
      </div>
  );
}

export default AddAttackerOrTarget;
