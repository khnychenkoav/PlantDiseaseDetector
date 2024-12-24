import React from 'react';
import UploadForm from './components/UploadForm';
import ResultView from './components/ResultView';
import GardenMap from './components/GardenMap';

function App() {
    return (
        <div>
            <h1>Plant Disease Detector</h1>
            <UploadForm />
            <ResultView result="No data yet." />
            <GardenMap />
        </div>
    );
}

export default App;
