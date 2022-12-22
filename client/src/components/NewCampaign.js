import React, { useState } from 'react';

function NewCampaign() {

    const [time, setTime] = useState('5');
    const [template, setTemplate] = useState('office365');
    const [message, setMessage] = useState('');
    const [resStatus, setresStatus] = useState();

    function handleTimeChange(value) {
        setTime(value);
    }

    function handleTemplateChange(value) {
        setTemplate(value);
    }

    function sendCampaign(event) {
        event.preventDefault();
        const reqOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify( { template: template, time: time } )
        };
        fetch('/new_campaign', reqOptions)
          .then(response => response.json())
          .then(data => {
            setMessage(data.message); 
            setresStatus(data.status)
        });
    }

    return (
      <div className="new-campaign">
            <h3>Add new campaign</h3>
            <form method = "post" onSubmit={sendCampaign}>
                <div className="input-new-campaign">
                    <label for = "name">Choose template</label>
                    <input type="radio" name="template" value="cisco" checked={template === 'cisco'} onChange={event => handleTemplateChange(event.target.value)}/> Cisco
                    <input type="radio" name="template" value="citrix" checked={template === 'citrix'} onChange={event => handleTemplateChange(event.target.value)} /> Citrix
                    <input type="radio" name="template" value="domino" checked={template === 'domino'} onChange={event => handleTemplateChange(event.target.value)} /> Domino
                    <input type="radio" name="template" value="junipervpn" checked={template === 'junipervpn'} onChange={event => handleTemplateChange(event.target.value)} /> JuinperVPN
                    <input type="radio" name="template" value="office365" checked={template === 'office365'} onChange={event => handleTemplateChange(event.target.value)} /> Office365
                    <input type = "submit" value = "Submit" />
                </div>
                    <label for="time">campaign duartion (in minutes):</label>
                    <input type="number" value={time} id="time" name="time" min={1} onChange={e => handleTimeChange(e.target.value)}/>
            </form>
            <p className='message' style={{color: resStatus === 200 ? 'green' : 'red'}}>{message ? message : null}</p>
        </div>
    );
  }
  
  export default NewCampaign;
  