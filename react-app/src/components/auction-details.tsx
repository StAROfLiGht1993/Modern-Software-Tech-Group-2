import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

// Define the Auction details type
interface AuctionDetail {
    AuctionID: number;
    title: string;
    Status: string;
    HighestBid: number;
    CardName: string;
    ImageURL: string;
}

// Define the bid request type
interface BidRequest {
    auction_id: number;
    user_id: number;
    HighestBid: number;
}

const BiddingPage: React.FC = () => {
    const { auctionID } = useParams<{ auctionID: string }>(); // Get auction ID from URL
    const [auction, setAuction] = useState<AuctionDetail | null>(null);
    const [bidAmount, setBidAmount] = useState<string>("");
    const [message, setMessage] = useState<string>("");

    useEffect(() => {
      if (auctionID) {
          fetchAuctionDetails();
        }
    }, [auctionID]); 

    const fetchAuctionDetails = async () => {
        try {
            const response = await axios.get<AuctionDetail>(
                `http://127.0.0.1:8000/bidding/auction-details/${auctionID}`
            );
            setAuction(response.data);
        } catch (error) {
            console.error("Error fetching auction details:", error);
        }
    };

    const handleBidChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setBidAmount(event.target.value);
    };

    const submitBid = async () => {
      if (!auction) return;
  
      const bidValue = parseFloat(bidAmount);
      if (isNaN(bidValue) || bidValue <= auction.HighestBid) {
          setMessage("Bid must be higher than the current highest bid!");
          return;
      }
  
      try {
          const token = localStorage.getItem("authToken"); // ✅ Retrieve stored token
          if (!token) {
              setMessage("Please log in to place a bid.");
              return;
          }
  
          const bidData: BidRequest = {
              auction_id: auction.AuctionID,
              user_id: 1, // This should be removed; backend should get user from token
              HighestBid: bidValue
          };
  
          const response = await axios.post(
              "http://127.0.0.1:8000/bidding/place-bid",
              bidData,
              { headers: { Authorization: `Bearer ${token}` } } // ✅ Attach Auth Header
          );
  
          setMessage(response.data.message);
          setAuction((prev) => (prev ? { ...prev, HighestBid: bidValue } : prev)); // ✅ Update UI bid
      } catch (error) {
          console.error("Error placing bid:", error);
          setMessage("Failed to place bid. Please try again.");
      }
  };

    if (!auction) return <h2>Loading auction details...</h2>;

    return (
        <div style={{ padding: "20px", textAlign: "center" }}>
            <h2>Bidding for {auction.title}</h2>
            
            {/* Auction Image */}
            <img src={auction.ImageURL} alt={auction.CardName} width="300px" />

            {/* Auction Details */}
            <div style={{
                border: "1px solid #ddd",
                padding: "15px",
                marginTop: "15px",
                backgroundColor: "#f9f9f9",
                borderRadius: "5px"
            }}>
                <p><strong>Auction ID:</strong> {auction.AuctionID}</p>
                <p><strong>Status:</strong> {auction.Status}</p>
                <p><strong>Highest Bid:</strong> ${auction.HighestBid}</p>
                <p><strong>Card Name:</strong> {auction.CardName}</p>
            </div>

            {/* Bidding Input */}
            <div style={{ marginTop: "15px" }}>
                <input
                    type="number"
                    placeholder="Enter your bid"
                    value={bidAmount}
                    onChange={handleBidChange}
                    style={{ padding: "10px", width: "150px" }}
                />
                <button onClick={submitBid} style={{ marginLeft: "10px", padding: "10px 20px" }}>
                    Place Bid
                </button>
            </div>

            {/* Bid Status Message */}
            {message && <p style={{ color: "green", marginTop: "10px" }}>{message}</p>}
        </div>
    );
};

export default BiddingPage;

