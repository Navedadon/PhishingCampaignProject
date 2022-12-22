import React, { useState, useEffect } from 'react';

function CampaignData() {
   const [campaigns, setCamapigns] = useState([]);

   useEffect(() => {
      fetch('/campaign_data').then(response => {
         if(response.ok) return response.json()
      }).then(data => {console.log(data); setCamapigns(JSON.parse(data.campaigns))})
   },[])

return (
    <div className="campaign-data">
    <h1> Campaigns </h1>
      { campaigns.length !== 0 ?
      <div>
         <table>
            <thead>
               <tr>
                  <th>status</th>
                  <th>campaign number</th>
                  <th>passed number</th>
                  <th>failed number</th>
               </tr>
            </thead>

            <tbody>
               {campaigns.map((campaign) => 
                  <tr>
                     <td className='status' style={{color: campaign.is_alive === 'True' ? 'green' : 'red'}}>{campaign.is_alive === 'True' ? 'Alive' : 'Finished'}</td>
                     <td>{campaign.campaign_number}</td>
                     <td>{campaign.passed_number/(campaign.passed_number+campaign.failed_number)*100}%</td>
                     <td>{campaign.failed_number/(campaign.passed_number+campaign.failed_number)*100}%</td>
                  </tr>)}
            </tbody>
         </table>
      </div> : <p className='no-campaign'>No campaigns currently</p>}
    </div>
);
}

export default CampaignData;
