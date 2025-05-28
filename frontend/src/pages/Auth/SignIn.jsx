import * as Yup from "yup";
import { Form, Formik } from "formik";
import React from "react";
import axios from "../../services/axiosInstance";
import FormInput from "../../components/FormInput/FormInput";
import { toast } from "react-toastify";

export default function SignIn() {
  const initialValues = {
    email: "",
    password: "",
  };

  const validationSchema = Yup.object().shape({
    email: Yup.string().email("Invalid email address").required("Email is required"),
    password: Yup.string().required("Password is required"),
  });

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const response = await axios.post(
        '/auth/login/',
        {
          email: values.email,
          password: values.password
        }
      );
      localStorage.setItem("loggedIn", "true");

      const token = response.data.access_token;
      console.log("Response:", response.data);
      localStorage.setItem("accessToken", token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      toast.success("Signed in successfully!");
    } catch (error) {
      console.error("Error:", error.response ? error.response.data : error.message);
      if (error.response?.data?.detail) {
        const errorMessages = error.response.data.detail.map(err => err.msg).join(", ");
        toast.error(`Sign in failed: ${errorMessages}`);
      } else {
        toast.error("Sign in failed. Please try again.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <h2 className="text-center">Sign In</h2>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ isSubmitting }) => (
              <Form>
                <FormInput name="email" type="email" label="Email" />
                <FormInput name="password" type="password" label="Password" />
                <button type="submit" className="btn btn-primary w-100 mt-3" disabled={isSubmitting}>
                  {isSubmitting ? "Signing In..." : "Sign In"}
                </button>
              </Form>
            )}
          </Formik>
        </div>
      </div>
    </div>
  );
}
