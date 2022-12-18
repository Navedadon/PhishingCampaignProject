//import React, { useState, useEffect } from 'react';

function AddAttackerOrTarget() {

  return (
    <div className="add">
      <h3>Add attacker or target</h3>

        <form method = "post">
            <div className="radio-btn">
                <input type="radio" name="attacker_Target" value="target" checked /> Target
                <input type="radio" name="attacker_Target" value="attacker" /> Attacker
            </div>
            <div className="inputs">
                <label for = "name">Name</label>
                <input type = "text" name = "name" placeholder = "Name" />
                <label for = "email">Email</label>
                <input type = "text" name = "email" placeholder = "email" />
                <label for = "password">password</label>
                <input type = "text" name = "password" placeholder = "password" />
                <input type = "submit" value = "Submit" />
            </div>
        </form>
      </div>
  );
}

export default AddAttackerOrTarget;
