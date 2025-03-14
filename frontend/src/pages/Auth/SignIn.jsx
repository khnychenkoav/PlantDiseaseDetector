import * as Yup from "yup";

import { Form, Formik } from "formik";
import React from "react";

import FormInput from "../../components/FormInput/FormInput";
import { toast } from "react-toastify";

export default function SignIn() {
  const initialValues = {
      email: "",
      password: "",
    },
    validationSchema = Yup.object().shape({
      email: Yup.string().email().required(),
      password: Yup.string().required(),
    }),
    handleSubmit = async (values) => {
      // Handle sign-in logic here
      toast.success("Signed in successfully!");
    };

  return (
    <div className='container'>
      <div className='row justify-content-center'>
        <div className='col-md-6'>
          <h2 className='text-center'>Sign In</h2>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={(values) => handleSubmit(values)}
          >
            <Form>
              <FormInput name='email' type='email' />
              <FormInput name='password' type='password' />
              <button type='submit' className='btn btn-primary w-100 mt-3'>
                Sign In
              </button>
            </Form>
          </Formik>
        </div>
      </div>
    </div>
  );
}
