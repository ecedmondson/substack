import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

const API_BASE = '/api/contact';

const fetchJSON = async (url, options = {}) => {
  const res = await fetch(url, options);
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || res.statusText);
  }
  return res.json();
};

export const useContactList = () => {
  return useQuery({
    queryKey: ['contacts'],
    queryFn: () => fetchJSON(API_BASE),
  });
};

export const useContactDetail = (id) => {
  return useQuery({
    queryKey: ['contact', id],
    queryFn: () => fetchJSON(`${API_BASE}/${id}`),
    enabled: !!id,
  });
};

export const useCreateContact = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (newContact) =>
      fetchJSON(API_BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newContact),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contacts'] });
    },
  });
};

export const useUpdateContact = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, updatedData }) =>
      fetchJSON(`${API_BASE}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedData),
      }),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['contacts'] });
      queryClient.invalidateQueries({ queryKey: ['contact', id] });
    },
  });
};
