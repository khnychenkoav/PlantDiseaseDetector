import React, { useEffect, useState } from "react";
import axios from "../../services/axiosInstance";
import "./DiseasesList.scss";

export default function DiseasesList() {
  const [diseases, setDiseases] = useState([]);

  useEffect(() => {
    const fetchDiseases = async () => {
      try {
        const response = await axios.get("/diseases/all");
        setDiseases(response.data);
      } catch (error) {
        console.error("Error fetching diseases:", error);
      }
    };

    fetchDiseases();
  }, []);

  return (
    <div className='container diseases-list'>
      <div className='row justify-content-center'>
        <div className='col-md-8'>
          <h1 className='text-center mb-4'>Diseases List</h1>
          <ul className='list-group'>
            {diseases.map((disease) => (
              <li key={disease.id} className='list-group-item'>
                <h5>{disease.name}</h5>
                <p>{disease.description}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
