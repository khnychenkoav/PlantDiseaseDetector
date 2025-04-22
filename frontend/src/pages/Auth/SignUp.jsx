import * as Yup from "yup";
import { Form, Formik } from "formik";
import React from "react";
import axios from "axios";
import FormInput from "../../components/FormInput/FormInput";
import { toast } from "react-toastify";

export default function SignUp() {
  const initialValues = {
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  };

  const validationSchema = Yup.object().shape({
    name: Yup.string()
      .min(3, "Name must be at least 3 characters")
      .max(20, "Name cannot exceed 20 characters")
      .required("Name is required"),
    email: Yup.string().email("Invalid email address").required("Email is required"),
    password: Yup.string()
      .min(7, "Password must be at least 7 characters")
      .max(20, "Password cannot exceed 20 characters")
      .required("Password is required"),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref("password"), null], "Passwords must match")
      .required("Confirm Password is required"),
  });

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const response = await axios.post(
        'http://localhost:8080/auth/register',
        {
          email: values.email,
          password: values.password,
          name: values.name
        },
        {
          headers: { 'Content-Type': 'application/json' },
          'Accept': 'application/json'
        }
      );
      
      
  
      console.log("Response:", response.data);
      toast.success("Signed up successfully!");
    } catch (error) {
      console.error("Error:", error.response ? error.response.data : error.message);
      
      if (error.response?.data?.detail) {
        const errorMessages = error.response.data.detail.map(err => err.msg).join(", ");
        toast.error(`Sign up failed: ${errorMessages}`);
      } else {
        toast.error("Sign up failed. Please try again.");
      }
    } finally {
      setSubmitting(false);
    }
  };
  

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <h2 className="text-center">Sign Up</h2>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ isSubmitting }) => (
              <Form>
                <FormInput name="name" type="text" label="Name" />
                <FormInput name="email" type="email" label="Email" />
                <FormInput name="password" type="password" label="Password" />
                <FormInput name="confirmPassword" type="password" label="Confirm Password" />
                <button type="submit" className="btn btn-primary w-100 mt-3" disabled={isSubmitting}>
                  {isSubmitting ? "Signing Up..." : "Sign Up"}
                </button>
              </Form>
            )}
          </Formik>
        </div>
      </div>
    </div>
  );
}
