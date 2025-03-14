import React from "react";
import "./History.scss";

export default function History() {
  const historyData = [
    {
      id: 1,
      date: "2025-03-10",
      plant: "Tomato",
      disease: "Late Blight",
      treatment: "Apply fungicide",
    },
    {
      id: 2,
      date: "2025-03-12",
      plant: "Rose",
      disease: "Black Spot",
      treatment: "Remove affected leaves",
    },
  ];

  return (
    <div className='container history'>
      <div className='row justify-content-center'>
        <div className='col-md-8'>
          <h1 className='text-center mb-4'>History</h1>
          <table className='table table-bordered'>
            <thead>
              <tr>
                <th>Date</th>
                <th>Plant</th>
                <th>Disease</th>
                <th>Treatment</th>
              </tr>
            </thead>
            <tbody>
              {historyData.map((entry) => (
                <tr key={entry.id}>
                  <td>{entry.date}</td>
                  <td>{entry.plant}</td>
                  <td>{entry.disease}</td>
                  <td>{entry.treatment}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
