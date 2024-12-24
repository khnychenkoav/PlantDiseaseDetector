import React from 'react';

function ResultView({ result }) {
    return (
        <div>
            <h2>Analysis Result</h2>
            <p>{result}</p>
        </div>
    );
}

export default ResultView;
