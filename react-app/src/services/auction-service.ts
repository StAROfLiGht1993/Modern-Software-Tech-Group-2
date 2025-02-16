import axios from "axios";

export interface Auction {
  AuctionID: number;
  title: string;
  HighestBid: number;
  Status: string;
  EndTime: string;
}

export interface AuctionResponse {
  auctions: Auction[];
  total_pages: number;
}

// Fetch Auctions with Pagination
export const fetchAuctions = async (page: number = 1): Promise<AuctionResponse> => {
  try {
    const response = await axios.get<AuctionResponse>(`http://127.0.0.1:8000/auctions/?page=${page}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching auctions:", error);
    return { auctions: [], total_pages: 1 }; // ✅ Correctly return an object with properties
  }
};


// Define Interface for Bidding
export interface BidRequest {
  AuctionID: number;
  BidAmount: number;
}

// Submit a Bid
export const placeBid = async (bid: BidRequest): Promise<{ message: string; new_highest_bid: number } | null> => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/bid/", bid);
    return response.data; // Axios handles JSON automatically
  } catch (error) {
    console.error("Error placing bid:", error);
    return null;
  }
};

