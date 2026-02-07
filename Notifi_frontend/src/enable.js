import { messaging } from "./firebase";
import { getToken } from "firebase/messaging";

export async function enableNotifications() {
  const permission = await Notification.requestPermission();

  if (permission !== "granted") return;

  const token = await getToken(messaging, {
    vapidKey: "BPzNQHVx6sQt2dy6YjeMYjmaQ5V1tc9Tubrqes9Ele4Hrw5OeZu7msxCDJ229axD4-dQXazMnuzd6Ev2PRg6u3Q"
  });

  if (!token) {
    console.error("❌ No token generated");
    return;
  }

  console.log("✅ FCM token:", token);

  let deviceId = localStorage.getItem("deviceId");
  if (!deviceId) {
    deviceId = crypto.randomUUID();
    localStorage.setItem("deviceId", deviceId);
  }

  await fetch("http://localhost:8000/save-token", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ deviceId, token })
  });

  console.log("✅ Token saved");
}
