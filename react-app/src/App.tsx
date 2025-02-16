import { Routes, Route, Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import Logo from "./assets/logo.svg.png"; // Ensure the file exists in src/assets

// Components
import AuctionList from "./components/list-grp";
import AuctionDetails from "./components/auction-details";
import SearchPage from "./components/SearchPage";

// Services
import { fetchSearchResults } from "./services/searchpage-service";

// Type definition for search results
// interface SearchResult {
//   id: string;
//   CardName?: string;
//   Username?: string;
// }

// // Function to fetch search results
// const fetchSearchResults = async (
//   query: string,
//   setResults: (results: SearchResult[]) => void,
//   setLoading: (loading: boolean) => void
// ) => {
//   setLoading(true);
//   try {
//     const [cardResponse, profileResponse] = await Promise.all([
//       axios.get(`http://localhost:8000/search/cards?search_query=${query}`),
//       axios.get(`http://localhost:8000/search/profiles?search_query=${query}`)
//     ]);

//     // Combine both results
//     setResults([...cardResponse.data, ...profileResponse.data]);
//   } catch (error) {
//     console.error("Error during search", error);
//   } finally {
//     setLoading(false);
//   }
// };

function App() {
  return (
    <div className="max-w-2xl bg-white">
      {/* Logo */}
      <img src={Logo} alt="Auction Finder Logo" className="w-10 mb-1 mx-auto py-2" />
      {/* Navigation Panel */}
      <div className="items-center text-center bg-white">
        <div className= "space-y-2">
          <Link to="/">
            <button className="w-full px-4 py-2 text-black bold-text">
              Main
            </button>
          </Link>
          <Link to="/auction/:id">
            <button className="w-full px-4 py-2 text-black bold-text">
              Auction Details
            </button>
          </Link>
          <Link to="/search">
            <button className="w-full px-4 py-2 text-black bold-text">
              Search for cards
            </button>
          </Link>
          <Link to="/login">
            <button className="w-full px-4 py-2 text-black bold-text">
              Log in
            </button>
          </Link>
        </div>
      </div>

      {/* App Routes */}
      <div className="mt-8">
        <Routes>
          <Route path="/" element={<AuctionList />} />
          <Route path="/auction/:id" element={<AuctionDetails />} />
          <Route path="/search" element={<SearchPage fetchSearchResults={fetchSearchResults} />} />
        </Routes>
      </div>
    </div>

  );
}

export default App;