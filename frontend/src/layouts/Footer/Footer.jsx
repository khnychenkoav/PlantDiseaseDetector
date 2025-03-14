import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

export default function Footer() {
  return (
    <footer className='footer-gradient py-5 mt-5'>
      <div className='container'>
        <div className='row'>
          <div className='col'>
            <Link to='/' className='navbar-brand fs-2 fw-bold'>
              Plant Disease <span className='text-secondary'>Detector</span>
            </Link>
            <p className='text-muted'>
              The Plant Disease Detector project is designed to identify plant diseases using image recognition and provide users with recommendations for treatment and prevention. Users can upload plant images, and the system will analyze them, determine possible diseases, and provide detailed information about the problem and its solution.
            </p>
            <div className='text-center align-items-center'>
              <a href='mailto:ahmet4cetinkaya@outlook.com' className='text-muted text-decoration-none link-muted'>
                <i className='bi bi-envelope text-primary' /> mail@mail.com
              </a>
            </div>
          </div>
          <div className='col px-5'>
            <p className='fw-bold fs-2 text-secondary'>Useful Links</p>
            <ul className='list-group'>
              <li className='list-group-item ps-0 border-0'>
                <Link to='/detect-disease' className='text-muted text-decoration-none'>
                  Detect Disease
                </Link>
              </li>
              <li className='list-group-item ps-0 border-0'>
                <Link to='/diseases-list' className='text-muted text-decoration-none'>
                  Diseases List
                </Link>
              </li>
              <li className='list-group-item ps-0 border-0'>
                <Link to='/about' className='text-muted text-decoration-none'>
                  About Us
                </Link>
              </li>
              <li className='list-group-item ps-0 border-0'>
                <Link to='/history' className='text-muted text-decoration-none'>
                  History
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}
