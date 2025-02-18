import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Auction, fetchAuctions } from "../services/auction-service";
import axios from "axios";

// Define the Auction type based on FastAPI response
interface Auction {
  AuctionID: number;
  CardID: number;
  title: string;
  Status: string;
  HighestBid: number;
  IsValidated: boolean;
  CardName: string;
  CardQuality: string;
  ImageURL: string;
}

const AuctionList: React.FC = () => {
  const [auctions, setAuctions] = useState<Auction[]>([]);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [inputPage, setInputPage] = useState<string>("");
  const navigate = useNavigate();


  const fetchAuctions = async (pageNumber:number) => {
    try {
      const response = await axios.get<{ auctions: Auction[]; total_pages: number }>(
        `http://127.0.0.1:8000/bidding/auction-collection?page=${pageNumber}`
    );
      setAuctions(response.data.auctions);
      setTotalPages(response.data.total_pages);
  } catch (error) {
      console.error("Error fetching auctions:", error);
   }
  };

  useEffect(() => {
    fetchAuctions(page);
  }, [page]); // Fetch auctions when page changes

  const handlePageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setInputPage(event.target.value);
  };

  const goToPage = () => {
    const pageNumber = parseInt(inputPage);
    if (!isNaN(pageNumber) && pageNumber >= 1 && pageNumber <= totalPages) {
        setPage(pageNumber);
    } else {
        alert("Invalid page number");
    }
  };

  const goToBiddingPage = (auctionID: number) => {
    navigate(`/bidding/${auctionID}`);
  };


  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
        <h2>Live Auctions</h2>

        {/* Auction Grid */}
        <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)", // Two cards per row
            gap: "20px",
            justifyContent: "center",
            marginTop: "20px"
        }}>
            {auctions.map((auction) => (
                <div key={auction.AuctionID} style={{
                    border: "1px solid #ddd",
                    borderRadius: "10px",
                    padding: "10px",
                    textAlign: "center",
                    backgroundColor: "#fff",
                    boxShadow: "2px 2px 10px rgba(0, 0, 0, 0.1)"
                }}>
                    {/* Clickable Image */}
                    <img
                        src={auction.ImageURL}
                        alt={auction.CardName}
                        width="100%"
                        style={{ borderRadius: "5px", cursor: "pointer" }}
                        onClick={() => goToBiddingPage(auction.AuctionID)}
                    />

                    {/* Auction Details */}
                    <div style={{
                        marginTop: "10px",
                        padding: "10px",
                        borderTop: "1px solid #ddd",
                        textAlign: "left"
                    }}>
                        <p><strong>Auction ID:</strong> {auction.AuctionID}</p>
                        <p><strong>Title:</strong> {auction.title}</p>
                        <p><strong>Status:</strong> {auction.Status}</p>
                        <p><strong>Highest Bid:</strong> ${auction.HighestBid}</p>
                        <p><strong>Card Name:</strong> {auction.CardName}</p>
                    </div>
                </div>
            ))}
        </div>

        {/* Pagination Controls */}
        <div style={{ marginTop: "20px" }}>
            <button onClick={() => setPage((prev) => Math.max(prev - 1, 1))} disabled={page === 1}>
                Previous
            </button>

            <span style={{ margin: "0 10px" }}> Page {page} of {totalPages} </span>

            <button onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))} disabled={page === totalPages}>
                Next
            </button>

            {/* Page Number Input */}
            <input
                type="number"
                value={inputPage}
                onChange={handlePageChange}
                placeholder="Go to page"
                style={{ marginLeft: "10px", padding: "5px", width: "60px" }}
            />
            <button onClick={goToPage} style={{ marginLeft: "5px" }}>Go</button>
        </div>
    </div>
);
};

export default AuctionList;