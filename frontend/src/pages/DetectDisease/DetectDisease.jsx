import * as Yup from "yup";

import { Form, Formik } from "formik";
import React, { useState } from "react";

import FormFileInput from "../../components/FormFileInput/FormFileInput";
import { toast } from "react-toastify";
import axios from "axios";

export default function DetectDisease() {
  const [result, setResult] = useState(null);

  const initialValues = {
      image: null,
    },
    validationSchema = Yup.object().shape({
      image: Yup.mixed().required("Image is required"),
    }),
    handleSubmit = async (values) => {
      const formData = new FormData();
      formData.append("image", values.image);

      try {
        const response = await axios.post("/api/analyze", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        setResult(response.data);
        toast.success("Image analyzed successfully!");
      } catch (error) {
        toast.error("Failed to analyze image");
      }
    };

  return (
    <div className='container'>
      <div className='row justify-content-center'>
        <div className='col-md-6'>
          <h2 className='text-center'>Detect Disease</h2>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={(values) => handleSubmit(values)}
          >
            <Form>
              <FormFileInput name='image' accept='image/*' />
              <button type='submit' className='btn btn-primary w-100 mt-3'>
                Analyze
              </button>
            </Form>
          </Formik>
          {result && (
            <div className='mt-4'>
              <h3>Result</h3>
              <p><strong>Disease:</strong> {result.disease}</p>
              <p><strong>Treatment:</strong> {result.treatment}</p>
              <p><strong>Prevention:</strong> {result.prevention}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
