import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const RELAY_BASE = '/api/relay';

const fetchJSON = async (url, options = {}) => {
  const res = await fetch(url, options);
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || res.statusText);
  }
  return res.json();
};

export const useRuleList = () => {
  return useQuery({
    queryKey: ['rules'],
    queryFn: () => fetchJSON(`${RELAY_BASE}/rule`),
  });
};

export const useAddRuleToConfig = (contactId) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ config_id, rule_id }) =>
      fetchJSON(`${RELAY_BASE}/config/rule/enable`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ config_id, rule_id }),
      }),
    onSuccess: (_, { config_id }) => {
      // Invalidate queries to refetch updated data
      queryClient.invalidateQueries({ queryKey: ['contact', contactId] })
    },
  });
};


export const useDisableRuleInConfig = (contactId) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ config_id, rule_id }) =>
      fetchJSON(`${RELAY_BASE}/config/rule/disable`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ config_id, rule_id }),
      }),
    onSuccess: (_, { config_id }) => {
      // Invalidate queries to refetch updated data
      queryClient.invalidateQueries({ queryKey: ['contact', contactId] });
    },
  });
};
