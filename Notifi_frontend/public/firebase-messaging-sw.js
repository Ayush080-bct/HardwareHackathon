importScripts('https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyDJPSelcs-DHI0ymbOmIQ8dcGf-TOc45Js",
  authDomain: "power-1c867.firebaseapp.com",
  projectId: "power-1c867",
  storageBucket: "power-1c867.firebasestorage.app",
  messagingSenderId: "843138229681",
  appId: "1:843138229681:web:4753e2bafaaa69efdc8990",
  measurementId: "G-1MWQN1S82H"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
  });
});
