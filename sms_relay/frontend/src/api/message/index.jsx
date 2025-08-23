import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

const API_BASE = '/api/forwarding';

async function getJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Error fetching ${url}: ${res.statusText}`);
  return res.json();
}

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
      queryKey: ['message'],
      queryFn: () => getJson(`${API_BASE}/message`),
      ...options,
    });
  }
  
