import React from "react";
import CreateAccountBanner from "./CreateAccountBanner";
import { Link } from "react-router-dom";
import Overlay from "./Overlay";
import Steps from "./Steps";
import "./Home.css";

export default function Home() {
  return (
    <div className='container-fluid gradient-background p-0'>
      <div className='container p-0'>
        <Overlay />
        <Steps />
        <div className='text-center mb-5'>
          <Link to='/detect-disease' className='btn btn-primary rounded shadow' style={{ padding: '15px 30px', fontSize: '18px' }}>
            Detect Your Treat
          </Link>
        </div>
        <CreateAccountBanner />
      </div>
    </div>
  );
}
