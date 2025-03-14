import React from 'react';

export default function Steps() {
  return (
    <div className='row px-5 my-5'>
      <div className='col'>
        <h1 className='fw-bold display-5'>
          <span className='text-secondary'>Follow</span> <br /> Easy 4 Steps
        </h1>
        <p className='text-muted mt-4'>
          Our AI-powered tool helps you quickly identify plant diseases and provides expert recommendations on treatment and prevention.
        </p>
        <p className='text-muted'>
          ✅ Fast & Accurate – AI-driven diagnosis in seconds.
        </p>
        <p className='text-muted'>
          ✅ Comprehensive Database – Covers a wide range of plant diseases.
        </p>
        <p className='text-muted'>
          ✅ Preventive Measures – Learn how to protect other plants from infections.
        </p>
        <p className='text-muted'>
          ✅ User-Friendly – Simple and intuitive interface for all users.
        </p>
        <p className='text-muted'>
          Join us in making plant care easier and more efficient with cutting-edge AI technology. Try it now!
        </p>
      </div>
      <div className="d-flex flex-column align-items-center">
      <div className="text-center my-3">
        <i className="bi bi-person fs-1 text-primary"></i>
        <div className="fw-bold">Create an Account</div>
        <div className="text-muted px-3">Sign up to access our AI-powered plant disease detection tool.</div>
      </div>

      <div className="text-center my-3">
        <i className="bi bi-upload fs-1 text-success"></i>
        <div className="fw-bold">Upload a Photo</div>
        <div className="text-muted px-3">Take or upload a clear image of your plant for analysis.</div>
      </div>

      <div className="text-center my-3">
        <i className="bi bi-search fs-1 text-danger"></i>
        <div className="fw-bold">Get Diagnosis</div>
        <div className="text-muted px-3">Our AI model will analyze your plant and detect possible diseases.</div>
      </div>

      <div className="text-center my-3">
        <i className="bi bi-check2-circle fs-1 text-secondary"></i>
        <div className="fw-bold">Treat Your Plant</div>
        <div className="text-muted px-3">Receive expert recommendations to help your plant recover.</div>
      </div>

        
      </div>


    </div>
  );
}
