
function CampaignData() {

return (
    <div className="campaign-data">
    <h1> Campaigns: </h1>
      <table>
         <thead>
            <tr>
               <th>campaign number</th>
               <th>passed number</th>
               <th>failed number</th>
            </tr>
         </thead>

         <tbody>
               <tr>
                  <td>12548</td>
                  <td>58%</td>
                  <td>32% </td>
               </tr>
         </tbody>
      </table>
    </div>
);
}

export default CampaignData;
