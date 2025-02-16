import React from 'react';

interface SearchResult {
  id: string;
  CardName?: string;
  Username?: string;
}

interface SearchResultsProps {
  results: SearchResult[];
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  return (
    <div>
      {results.map((result) => (
        <div key={result.id}>
          {result.CardName ? <p>Card: {result.CardName}</p> : <p>Profile: {result.Username}</p>}
        </div>
      ))}
    </div>
  );
};

export default SearchResults;