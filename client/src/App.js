// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Login from './Components/Login/AuthForm';
import Register from './Components/Register/Register';
import { DataProvider } from './Context/DataContext';
import { UserProvider } from './Context/UserContext';

function App() {
  return (
    <Router>
      <UserProvider>
        <DataProvider>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Routes>
        </DataProvider>
        </UserProvider>
    </Router>
  );
}

export default App;
