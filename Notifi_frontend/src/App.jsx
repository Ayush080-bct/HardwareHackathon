import { useEffect, useState } from "react";
import Header from "./Components/Header";
import "./App.css";
import { enableNotifications } from "./enable";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    let ws;
    let reconnectTimer;

    const connect = () => {
      ws = new WebSocket("ws://localhost:8000/ws");

      ws.onmessage = (event) => {
        setData(JSON.parse(event.data));
      };

      ws.onclose = () => {
        reconnectTimer = setTimeout(connect, 1000);
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

      {/* ✅ REQUIRED BUTTON */}
      <button onClick={enableNotifications}>
        Enable Notifications
      </button>

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
