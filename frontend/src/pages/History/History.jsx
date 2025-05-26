import React, { useEffect, useState } from "react";
import axiosInstance from "../../services/axiosInstance";
import "./History.scss";

export default function History() {
  const [historyData, setHistoryData] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        console.log("axiosInstance:", axiosInstance);
        const response = await axiosInstance.get("/history/all", {
          withCredentials: true,
        });

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
        <div className='col-md-10'>
          <h1 className='text-center mb-4'>History</h1>
          <table className='table table-bordered'>
            <thead>
              <tr>
                <th>Date</th>
                <th>Disease</th>
                <th>Recommendation</th>
                <th>Image</th>
              </tr>
            </thead>
            <tbody>
              {historyData.map((entry, index) => (
                <tr key={index}>
                  <td>{entry.time}</td>
                  <td>{entry.diseases_name?.replaceAll("__", " ") || "-"}</td>
                  <td>{entry.recommendation || entry.reason || "-"}</td>
                  <td>
                    {entry.image_url ? (
                      <a href={`http://api.plantdetector.ru/${entry.image_url}`} target="_blank" rel="noreferrer">
                        <img
                          src={`http://api.plantdetector.ru/${entry.image_url}`}
                          alt="plant"
                          style={{ width: "80px", height: "80px", objectFit: "cover", borderRadius: "6px" }}
                        />
                      </a>
                    ) : (
                      "-"
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
