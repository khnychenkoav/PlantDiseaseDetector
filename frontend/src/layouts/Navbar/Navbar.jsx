import "./Navbar.scss";
import { Link, useHistory } from "react-router-dom";
import NavItem from "./NavItem";
import React, { useEffect, useState } from "react";
import axios from "../../services/axiosInstance";

export default function Navbar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const history = useHistory();

  useEffect(() => {
    const loggedIn = localStorage.getItem("loggedIn");
    if (loggedIn === "true") {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = async () => {
    try {
      await axios.post("/users/logout/");
      localStorage.removeItem("loggedIn");
      setIsAuthenticated(false);
      history.push("/signin");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <nav className='navbar navbar-expand-lg navbar-light py-3'>
      <div className='container'>
        <Link to='/' className='navbar-brand fs-2 fw-bold'>
          Plant Disease <span className='text-secondary'>Detector</span>
        </Link>
        <button
          className='navbar-toggler'
          type='button'
          data-bs-toggle='collapse'
          data-bs-target='#navbarmenu'
          aria-controls='navbarmenu'
          aria-expanded='false'
          aria-label='Toggle navigation'
        >
          <span className='navbar-toggler-icon' />
        </button>
        <div className='collapse navbar-collapse' id='navbarmenu'>
          <ul className='navbar-nav me-auto mb-2 mb-lg-0 w-100 justify-content-center'>
            <NavItem linkTo='' name='Home' iconClassName='bi bi-house' />
            <NavItem linkTo='/detect-disease' name='Detect Disease' iconClassName='bi bi-search' />
            <NavItem linkTo='/about' name='About Us' iconClassName='bi bi-info-circle' />
            <NavItem linkTo='/history' name='History' iconClassName='bi bi-card-text' />
          </ul>
        </div>
        <div>
          {isAuthenticated ? (
            <button
              className='btn btn-primary py-2 px-4 rounded shadow'
              onClick={handleLogout}
            >
              Log out
            </button>
          ) : (
            <>
              <Link
                to='/signup'
                className='btn btn-outline-primary me-4 py-2 px-4 rounded shadow'
              >
                Sign up
              </Link>
              <Link
                to='/signin'
                className='btn btn-primary py-2 px-4 rounded shadow'
              >
                Log in
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
