// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getMessaging } from "firebase/messaging";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDJPSelcs-DHI0ymbOmIQ8dcGf-TOc45Js",
  authDomain: "power-1c867.firebaseapp.com",
  projectId: "power-1c867",
  storageBucket: "power-1c867.firebasestorage.app",
  messagingSenderId: "843138229681",
  appId: "1:843138229681:web:4753e2bafaaa69efdc8990",
  measurementId: "G-1MWQN1S82H"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const messaging = getMessaging(app);