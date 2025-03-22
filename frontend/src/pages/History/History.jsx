import React, { useEffect, useState } from "react";
import axiosInstance from "../../services/axiosInstance";
import "./History.scss";

export default function History() {
  const [historyData, setHistoryData] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axiosInstance.get("/history/all");
        setHistoryData(response.data);
      } catch (error) {
        console.error("Error fetching history data:", error);
      }
    };

    fetchHistory();
  }, []);

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
                  <td>{entry.time}</td>
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
