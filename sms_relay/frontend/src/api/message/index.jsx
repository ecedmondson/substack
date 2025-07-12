import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

// Base API URL prefix
const API_BASE = '/api/forwarding';

// Helper: GET JSON
async function getJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Error fetching ${url}: ${res.statusText}`);
  return res.json();
}

/**
 * useMessageDetail
 * GET /api/forwarding/message/{id}
 * 
 * @param {string} id - UUID of message to fetch
 * @param {object} options - react-query query options
 * @returns query object with data, error, isLoading etc
 */
 export function useMessageDetail(id, options = {}) {
    return useQuery({
      queryKey: ['message', id],
      queryFn: () => getJson(`${API_BASE}/message/${id}`),
      enabled: !!id,
      ...options,
    });
  }
  

export function useMessagesList(options = {}) {
    return useQuery({
      queryKey: ['messages'],
      queryFn: () => getJson(`${API_BASE}/messages`),
      ...options,
    });
  }
  
