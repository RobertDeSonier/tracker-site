// Navbar.js - Navigation bar component
import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../utils/AuthContext';
import './Navbar.css';

function Navbar() {
  const { isLoggedIn, logout } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="navbar-brand">Tracker</Link>
        <ul className="navbar-links">
          <li><Link to="/">Home</Link></li>
          {!isLoggedIn && <li><Link to="/login">Login</Link></li>}
          {isLoggedIn && <li><Link to="/dashboard">Dashboard</Link></li>}
          {isLoggedIn && <li><Link to="/profile">Profile</Link></li>}
          {isLoggedIn && <li><button onClick={logout}>Logout</button></li>}
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;