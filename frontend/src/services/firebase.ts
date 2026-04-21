import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { connectFirestoreEmulator } from 'firebase/firestore';
import { connectAuthEmulator } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyDlKujiaqB4zUiSRGLkVZikyfiA8yDUVKQ",
  authDomain: "fast-queue-493301.firebaseapp.com",
  projectId: "fast-queue-493301",
  storageBucket: "fast-queue-493301.firebasestorage.app",
  messagingSenderId: "301062546773",
  appId: "1:301062546773:web:c47fb788cfe555a5e4fbdc"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);

if (location.hostname === "localhost") {
  connectAuthEmulator(auth, "http://127.0.0.1:9099", { disableWarnings: true });
  connectFirestoreEmulator(db, "127.0.0.1", 8080);
  console.log("🛠️  Frontend conectado aos emuladores em 127.0.0.1");
}

export default app;