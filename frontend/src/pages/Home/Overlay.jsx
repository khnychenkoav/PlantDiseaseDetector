import React from "react";
import overlayVector from "../../assets/images/overlay-vector.svg";
import { Link } from "react-router-dom/cjs/react-router-dom.min";
import { useHistory } from 'react-router-dom';

export default function Overlay() {
  const history = useHistory();
  const handleDetectClick = () => {
    history.push('/detect-disease');
  };
  return (
    <div className='row' style={{ margin: 0 }}>
      <div className='col-md-6 d-flex flex-column justify-content-center p-0'>
        <section 
          id='job-advert-search' 
          className='d-flex flex-column justify-content-center align-items-center text-center w-100'
          style={{ padding: '20px' }} // Добавлен внутренний отступ для красоты
        >
          <div className='w-100'>
            <h1 className='display-1 fw-bold text-primary mb-3'>
              <span className='text-secondary'>Send. Read.</span> Treat
              <span className='text-secondary'>.</span>
            </h1>
            <h4 className='mb-4'>Your plant is waiting for you.</h4>
            <form className='w-100 p-2 d-flex flex-column align-items-center rounded-2 shadow'>
              <div className='input-group'>
                <button className='btn btn-primary p-2 rounded w-100' type='button' onClick={handleDetectClick}>
                    <i className='bi bi-search align-self-center me-1' /> Detect
                </button>
              </div>
            </form>
          </div>
        </section>
      </div>

      <div className='col-md-6 position-relative p-0'>
        <img 
          src={overlayVector} 
          alt='plant disease detector' 
          className='img-fluid h-100 w-100 d-none d-md-block' 
          style={{ objectFit: 'contain' }}
        />
        <img 
          src={overlayVector} 
          alt='plant disease detector mobile' 
          className='img-fluid d-md-none' 
          style={{ maxHeight: '300px' }}
        />
      </div>
    </div>
  );
}
