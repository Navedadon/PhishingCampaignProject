import React, { useState, useEffect } from 'react';

function AttackersTargetsTable() {

   const [attackers, setAttackers] = useState([]);
   const [targets, setTargets] = useState([]);

   useEffect(() => {
      fetch('/attackers_targets_info').then(response => {
         if(response.ok) return response.json()
      }).then(data => {
         setAttackers(JSON.parse(data.attackers)); 
         setTargets(JSON.parse(data.targets));
      })
   },[])

   function handleRemove(event, type, info){
      event.preventDefault();
        const reqOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify( { type: type, name: info } )
        };
      fetch('/remove_attacker_or_target', reqOptions)
          .then(response => response.json())
          .then(data => {
            setAttackers(JSON.parse(data.attackers)); 
            setTargets(JSON.parse(data.targets));
        });
   }

  return (
    <div className="table">
      <h2> Attackers </h2>
      {attackers.length !== 0 ? <div>
         <table>
            <thead>
               <tr>
                  <th></th>
                  <th>Name</th>
                  <th>Email</th>
               </tr>
            </thead>

            <tbody>
               {attackers.map((attacker) => 
                  <tr>
                     <td><button onClick={event => handleRemove(event, 'attacker', attacker.name)}>-</button></td>
                     <td>{attacker.name}</td>
                     <td>{attacker.email}</td>
                  </tr>)}
            </tbody>
         </table>
      </div> : <p className='no-attackers'>No campaigns currently</p>}
      <h2> Targets </h2>
      {targets.length !== 0 ? <div>
      <table>
            <thead>
               <tr>
                  <th></th>
                  <th>Name</th>
                  <th>Email</th>
               </tr>
            </thead>

            <tbody>
               {targets.map((target)=>
                  <tr>
                     <td><button onClick={event => handleRemove(event, 'target', target.name)}>-</button></td>
                     <td>{target.name}</td>
                     <td>{target.email}</td>
                  </tr>)}
            </tbody>
         </table>
         </div> : <p className='no-targets'>No campaigns currently</p>}
      </div>
  );
}

export default AttackersTargetsTable;
