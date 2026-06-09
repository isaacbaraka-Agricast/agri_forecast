import 'package:firebase_core/firebase_core.dart';

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform => web;

  static const FirebaseOptions web = FirebaseOptions(
    apiKey: "AIzaSyBWua0cfzAIFE1UIcJ_9tQGf4VuN1HsBfU",
    authDomain: "agri-forecast-f192d.firebaseapp.com",
    projectId: "agri-forecast-f192d",
    storageBucket: "agri-forecast-f192d.firebasestorage.app",
    messagingSenderId: "52854145362",
    appId: "1:52854145362:web:b3bce223274bea033cba8b",
  );
}