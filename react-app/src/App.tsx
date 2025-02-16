import { Routes, Route } from "react-router-dom";
import AuctionList from "./components/list-grp";
import BiddingPage from "./components/auction-details";

function App() {
  return (
    <div className="bg-gray-100 min-h-screen flex items-center justify-center p-6">
      <Routes>
        <Route path="/" element={<AuctionList />} />
        <Route path="/bidding/:auctionID" element={<BiddingPage />} />
      </Routes>
    </div>
  );
}

export default App;
