import React from "react";
import "./AboutUs.scss";
import logo from '../../assets/images/3818806.jpg';

export default function AboutUs() {
  return (
    <div className='container about-us'>
      <div className='row justify-content-center'>
        <div className='col-md-8'>
          <h1 className='text-center mb-4'>About Us</h1>
          <p className='lead text-center'>
            Welcome to Plant Disease Detector, your trusted partner in plant health.
          </p>
          <p>
            Our mission is to help you keep your plants healthy and thriving. Using advanced AI technology, we provide accurate and fast disease detection for a wide range of plants. Simply upload a photo of your plant, and our system will analyze it to identify any potential diseases and provide expert recommendations for treatment and prevention.
          </p>
          <p>
            Our team is composed of passionate plant enthusiasts, experienced data scientists, and skilled software engineers. We are dedicated to making plant care easier and more efficient for everyone, from home gardeners to professional farmers.
          </p>
          <p>
            Join us in our mission to promote plant health and sustainability. Together, we can make a difference, one plant at a time.
          </p>
          <div className='text-center mt-5'>
            <img src={logo} alt='Our Team' className='img-fluid rounded shadow' />
          </div>
        </div>
      </div>
    </div>
  );
}
