import React, { useState } from 'react';
import SearchBar from './SearchBar';



interface SearchPageProps {
  fetchSearchResults: (query: string) => Promise<any[]>;
}

const SearchPage: React.FC<SearchPageProps> = ({ fetchSearchResults }) => {
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSearch = async (query: string) => {
    setLoading(true);
    try {
      const searchResults = await fetchSearchResults(query);
      setResults(searchResults);
    } catch (error) {
      console.error("Error fetching search results", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      <SearchBar onSearch={handleSearch} />
      {loading && <p>Loading...</p>}
      <ul>
        {results.map((result, index) => (
          <li key={index}>{result.CardName || result.Username}</li>
        ))}
      </ul>
    </div>
  );
};

export default SearchPage;