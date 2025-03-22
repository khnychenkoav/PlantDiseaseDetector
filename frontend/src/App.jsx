import "bootstrap";
import "./App.scss";
import "react-toastify/dist/ReactToastify.css";

import { Route, BrowserRouter as Router, Switch } from "react-router-dom";

import DetectDisease from "./pages/DetectDisease/DetectDisease";
import Footer from "./layouts/Footer/Footer";
import Home from "./pages/Home/Home";
import Navbar from "./layouts/Navbar/Navbar";
import SignIn from "./pages/Auth/SignIn";
import SignUp from "./pages/Auth/SignUp";
import AboutUs from "./pages/AboutUs/AboutUs";
import History from "./pages/History/History";
import DiseasesList from "./pages/DiseasesList/DiseasesList";
import { ToastContainer } from "react-toastify";

function App() {
  return (
    <div id='App' className='d-flex flex-column'>
      <Router>
        <Navbar />
        <div style={{ paddingTop: "120px" }}>
          <main>
            <Switch>
              <Route exact path='/' component={Home} />
              <Route exact path='/signin' component={SignIn} />
              <Route exact path='/signup' component={SignUp} />
              <Route exact path='/detect-disease' component={DetectDisease} />
              <Route exact path='/about' component={AboutUs} />
              <Route exact path='/history' component={History} />
              <Route exact path='/diseases-list' component={DiseasesList} />
            </Switch>
          </main>
        </div>
        <Footer />
        <ToastContainer
          position='bottom-right'
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </Router>
    </div>
  );
}

export default App;
