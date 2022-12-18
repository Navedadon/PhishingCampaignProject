import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import './App.css';
import About from './components/About';
import AttackersTargetsTable from "./components/AttackersTargetsTable";
import AddAttackerOrTarget from "./components/AddAttackerOrTarget";
import NewCampaign from "./components/NewCampaign";
import CampaignData from "./components/CampaignData";

function App() {

  return (
    <div className="App">
        <Router>
          <div className="App-header">
            <Link className="App-link" to="/">Main</Link>
            <Link className="App-link" to="/attackers_targets_info">Attackers and targets tables</Link>
            <Link className="App-link" to="/add_attacker_or_target">Add attacker or target</Link>
            <Link className="App-link" to="/new_campaign">Start new campaign</Link>
            <Link className="App-link" to="/campaign_data">Campaign Data</Link>
          </div>
          <Routes>
            <Route exact path="/" element={<About/>}/>
            <Route exact path="attackers_targets_info" element={<AttackersTargetsTable/>}/>
            <Route exact path="add_attacker_or_target" element={<AddAttackerOrTarget/>}/>
            <Route exact path="new_campaign" element={<NewCampaign/>}/>
            <Route exact path="campaign_data" element={<CampaignData/>}/>
          </Routes>
        </Router>
      </div>
  );
}

export default App;
