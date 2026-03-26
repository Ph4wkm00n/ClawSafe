"use client";

import { useEffect, useRef, useState } from "react";

import { ClawSafeWebSocket, type WSMessage } from "@/lib/websocket";

export function useWebSocket() {
  const [connected, setConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);
  const wsRef = useRef<ClawSafeWebSocket | null>(null);

  useEffect(() => {
    const ws = new ClawSafeWebSocket();
    wsRef.current = ws;

    const unsubscribe = ws.onMessage((msg) => {
      setLastMessage(msg);
      if (msg.type === "pong") return; // Ignore heartbeat responses
    });

    // Track connection state
    const checkConnection = setInterval(() => {
      setConnected(ws.connected);
    }, 2000);

    ws.connect();

    return () => {
      unsubscribe();
      clearInterval(checkConnection);
      ws.close();
    };
  }, []);

  return { connected, lastMessage };
}
