import { useEffect, useState } from "react";
import Header from "./Components/Header";
import "./App.css";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    let ws;
    let reconnectTimer;

    const connect = () => {
      ws = new WebSocket("ws://localhost:8000/ws");

      ws.onopen = () => {
        console.log("WebSocket connected");
      };

      ws.onmessage = (event) => {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      };

      ws.onerror = (err) => {
        console.error("WebSocket error", err);
        ws.close();
      };

      ws.onclose = () => {
        console.log("WebSocket closed. Reconnecting...");
        reconnectTimer = setTimeout(connect, 1000); // retry after 1s
      };
    };

    connect();

    return () => {
      clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, []);

  return (
    <div className="Container">
      <Header />
      <main className="Mainpage">
        {data ? (
          <div className="cls">
            <p>Voltage: {data.voltage} V</p>
            <p>Current: {data.current} A</p>
            <h2 style={{ color: data.status === "OVERLOAD" ? "red" : "green" }}>
              Status: {data.status}
            </h2>
          </div>
        ) : (
          <p>Waiting for data...</p>
        )}
      </main>
    </div>
  );
}

export default App;
