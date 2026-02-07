import { useEffect, useState } from "react";
import Header from "./Components/Header";
import './App.css'

function App() {
  const [data, setData] = useState(null);

 useEffect(() => {
  const ws = new WebSocket("ws://localhost:8000/ws");

  ws.onopen = () => {
    console.log("WebSocket connected");
  };

  ws.onmessage = (event) => {
    console.log("Received:", event.data);
    setData(JSON.parse(event.data));
  };

  ws.onerror = (err) => {
    console.error("WebSocket error", err);
  };

  ws.onclose = () => {
    console.log("WebSocket closed");
  };

  return () => ws.close();
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
