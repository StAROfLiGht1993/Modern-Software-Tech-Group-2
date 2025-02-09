import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed

export const fetchSearchResults = async (query: string) => {
  try {
    const [cardResponse, profileResponse] = await Promise.all([
      axios.get(`${API_BASE_URL}/search/cards`, { params: { search_query: query } }),
      axios.get(`${API_BASE_URL}/search/profiles`, { params: { search_query: query } })
    ]);

    // Combine both results
    return [...cardResponse.data, ...profileResponse.data];
  } catch (error) {
    console.error("Error during search", error);
    throw error;
  }
};