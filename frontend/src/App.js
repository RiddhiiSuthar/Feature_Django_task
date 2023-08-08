import logo from './logo.svg';
import './App.css';
import React from 'react';
import EmailTrigger from './EmailTrigger'; // Adjust the path based on your project structure


function App() {
  return (
    <div className="App">
      <h1>Admin Dashboard</h1>
      <EmailTrigger />
      {/* Other components and content as needed */}
    </div>
  );
}

export default App;
