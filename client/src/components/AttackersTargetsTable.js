import React, { useState, useEffect } from 'react';

function AttackersTargetsTable() {

   const [attackers, setAttackers] = useState([]);
   const [targets, setTargets] = useState([]);

   useEffect(() => {
      fetch('/attackers_targets_info').then(response => {
         if(response.ok) return response.json()
      }).then(data => {setAttackers(JSON.parse(data.attackers)); setTargets(JSON.parse(data.targets))})
   },[])

  return (
    <div className="table">
      <h2> Attackers </h2>
      <table>
         <thead>
            <tr>
               <th>Name</th>
               <th>Email</th>
               <th>Password</th>
            </tr>
         </thead>

         <tbody>
            {attackers.map((attacker) => 
               <tr>
                  <td>{attacker.name}</td>
                  <td>{attacker.email}</td>
                  <td>{attacker.password}</td>
               </tr>)}
         </tbody>
      </table>
      <h2> Targets </h2>
      <table>
            <thead>
               <tr>
                  <th>Name</th>
                  <th>Email</th>
               </tr>
            </thead>

            <tbody>
               {targets.map((target)=>
                  <tr>
                     <td>{target.name}</td>
                     <td>{target.email}</td>
                  </tr>)}
            </tbody>
         </table>
      </div>
  );
}

export default AttackersTargetsTable;
