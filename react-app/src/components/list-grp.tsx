import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Auction, fetchAuctions } from "../services/auction-service";

const ListGrp: React.FC = () => {
  const [auctions, setAuctions] = useState<Auction[]>([]);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const navigate = useNavigate();

  useEffect(() => {
    loadAuctions();
  }, [page]); // Fetch auctions when page changes

  const loadAuctions = async () => {
    const response = await fetchAuctions(page); // ✅ Fetch full response
    setAuctions(response.auctions); // ✅ Now correctly extracts auctions
    setTotalPages(response.total_pages); // ✅ Now correctly extracts total pages
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-6 shadow-lg rounded-lg">
      <h1 className="text-2xl font-bold text-center mb-4">Live Auctions</h1>
      <div className="space-y-4">
        {auctions.length === 0 ? (
          <p className="text-center text-red-500">No auctions available.</p>
        ) : (
          auctions.map((auction) => (
            <div
              key={auction.AuctionID}
              className="p-4 bg-blue-100 rounded-lg shadow-md cursor-pointer hover:bg-blue-200"
              onClick={() => navigate(`/auction/${auction.AuctionID}`)}
            >
              <h2 className="text-lg font-semibold">{auction.title}</h2>
              <p><strong>Highest Bid:</strong> ${auction.HighestBid.toFixed(2)}</p>
              <p><strong>Status:</strong> {auction.Status}</p>
              <p><strong>Ends:</strong> {new Date(auction.EndTime).toLocaleString()}</p>
            </div>
          ))
        )}
      </div>

      {/* ✅ Pagination */}
      <div className="flex justify-center space-x-2 mt-4">
        <button
          className={`px-4 py-2 rounded ${page === 1 ? "bg-gray-300 cursor-not-allowed" : "bg-blue-500 text-white hover:bg-blue-600"}`}
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >
          Previous
        </button>
        {[...Array(totalPages)].map((_, index) => (
          <button
            key={index}
            className={`px-3 py-2 rounded ${page === index + 1 ? "bg-blue-600 text-white" : "bg-gray-300 hover:bg-gray-400"}`}
            onClick={() => setPage(index + 1)}
          >
            {index + 1}
          </button>
        ))}
        <button
          className={`px-4 py-2 rounded ${page === totalPages ? "bg-gray-300 cursor-not-allowed" : "bg-blue-500 text-white hover:bg-blue-600"}`}
          disabled={page === totalPages}
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default ListGrp;
