import * as Yup from "yup";

import { Form, Formik } from "formik";
import React from "react";

import FormInput from "../../components/FormInput/FormInput";
import { toast } from "react-toastify";

export default function SignUp() {
  const initialValues = {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
    validationSchema = Yup.object().shape({
      firstName: Yup.string().required(),
      lastName: Yup.string().required(),
      email: Yup.string().email().required(),
      password: Yup.string().required(),
      confirmPassword: Yup.string()
        .oneOf([Yup.ref("password"), null], "Passwords must match")
        .required(),
    }),
    handleSubmit = async (values) => {
      // Handle sign-up logic here
      toast.success("Signed up successfully!");
    };

  return (
    <div className='container'>
      <div className='row justify-content-center'>
        <div className='col-md-6'>
          <h2 className='text-center'>Sign Up</h2>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={(values) => handleSubmit(values)}
          >
            <Form>
              <FormInput name='firstName' type='text' />
              <FormInput name='lastName' type='text' />
              <FormInput name='email' type='email' />
              <FormInput name='password' type='password' />
              <FormInput name='confirmPassword' type='password' />
              <button type='submit' className='btn btn-primary w-100 mt-3'>
                Sign Up
              </button>
            </Form>
          </Formik>
        </div>
      </div>
    </div>
  );
}
