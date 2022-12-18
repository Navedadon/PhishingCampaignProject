//import React, { useState, useEffect } from 'react';

function NewCampaign() {
    return (
      <div className="new-campaign">
            <h3>Add new campaign</h3>
                <form method = "post">
                    <div className="input-new-campaign">
                        <label for = "name">Choose template</label>
                        <input type="radio" name="template" value="cisco" checked /> Cisco
                        <input type="radio" name="template" value="citrix" checked /> Citrix
                        <input type="radio" name="template" value="domino" checked /> Domino
                        <input type="radio" name="template" value="juinpervpn" checked /> JuinperVPN
                        <input type="radio" name="template" value="office365" checked /> Office365
                        <input type = "submit" value = "Submit" />
                    </div>
                </form>
        </div>
    );
  }
  
  export default NewCampaign;
  