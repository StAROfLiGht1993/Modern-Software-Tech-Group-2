import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Auction, fetchAuctions, placeBid } from "../services/auction-service";

const AuctionDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>(); // Get auction ID from URL
  const navigate = useNavigate();
  const [auction, setAuction] = useState<Auction | null>(null);
  const [bidAmount, setBidAmount] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const userId = 123; // ✅ Assume logged-in user ID (replace with actual logic)

  useEffect(() => {
    loadAuction();
  }, []);

  const loadAuction = async () => {
    const { auctions } = await fetchAuctions();
    const selectedAuction = auctions.find(a => a.AuctionID === Number(id));
    setAuction(selectedAuction || null);
  };

  const handleBid = async () => {
    const amount = parseFloat(bidAmount);
    if (isNaN(amount) || amount <= 0) {
      setMessage("Invalid bid amount.");
      return;
    }

    if (auction && amount > auction.HighestBid) {
      const bidResponse = await placeBid({
        AuctionID: auction.AuctionID,
        UserID: userId, // ✅ Send UserID to backend
        BidAmount: amount
      });

      if (bidResponse) {
        setMessage(`Bid placed successfully! New highest bid: $${bidResponse.new_highest_bid}`);
        loadAuction(); // Reload auction data after bid
      } else {
        setMessage("Failed to place bid. Ensure bid is higher than current highest bid.");
      }
    } else {
      setMessage("Bid must be higher than current highest bid.");
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 shadow-lg rounded-lg">
      <button onClick={() => navigate("/")} className="bg-gray-300 px-4 py-2 rounded mb-4">← Back</button>
      {auction ? (
        <>
          <h2 className="text-2xl font-bold">{auction.title}</h2>
          <p><strong>Highest Bid:</strong> ${auction.HighestBid.toFixed(2)}</p>
          <p><strong>Status:</strong> {auction.Status}</p>
          <p><strong>Ends:</strong> {new Date(auction.EndTime).toLocaleString()}</p>
          <div className="mt-4">
            <input
              type="number"
              min={auction.HighestBid + 1}
              value={bidAmount}
              onChange={(e) => setBidAmount(e.target.value)}
              className="p-2 border rounded w-32"
            />
            <button
              onClick={handleBid}
              className="ml-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Place Bid
            </button>
          </div>
          {message && <p className="mt-2 text-green-500">{message}</p>}
        </>
      ) : (
        <p className="text-red-500">Auction not found.</p>
      )}
    </div>
  );
};

export default AuctionDetails;
