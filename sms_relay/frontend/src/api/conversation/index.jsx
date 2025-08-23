import { useQuery, useMutation } from '@tanstack/react-query';

const fetchJSON = async (url, options = {}) => {
  const res = await fetch(url, options);
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || res.statusText);
  }
  return res.json();
};

export const useConversationThreads = (page = 0, pageSize = 15) => {
  return useQuery({
    queryKey: ['conversationThreads', page, pageSize],
    queryFn: () =>
      fetchJSON(
        `/api/conversation/thread?page=${page}&page_size=${pageSize}`
      ),
    keepPreviousData: true,
  });
};

export const useMessagesByThread = (threadId, page = 0, pageSize = 25) => {
  return useQuery({
    queryKey: ['messages', threadId, page, pageSize],
    queryFn: () =>
      fetchJSON(
        `/api/conversation/thread/${threadId}?page=${page}&page_size=${pageSize}`
      ),
    enabled: !!threadId,
    keepPreviousData: true,
  });
};

export const useRespondToThread = () => {
  return useMutation({
    mutationFn: async ({ threadId, payloadBody }) => {
      return fetchJSON(`/api/conversation/thread/${threadId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payloadBody),
      });
    },
  });
};