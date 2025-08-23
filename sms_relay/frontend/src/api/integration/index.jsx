import { useEffect, useState } from "react";


export function useTelnyxInboundWebSocket() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/api/integration/telnyx/inbound");

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    ws.onopen = () => console.log("Connected to Telnyx WS");
    ws.onclose = () => console.log("WS disconnected");

    return () => ws.close();
  }, []);

  return messages;
}