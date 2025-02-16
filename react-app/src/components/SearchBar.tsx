import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState<string>("");

  const handleSearch = () => {
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <main className="wrap max-w-2xl mx-auto bg-white text-center">
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Search for cards or profiles" 
        className="search-bar"
      />
      <button onClick={handleSearch} className="p-2 text-black rounded">
        Search
      </button>
    </main>
  );
}

export default SearchBar;