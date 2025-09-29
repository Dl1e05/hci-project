'use client'
import React, { useState, useEffect } from 'react';
import AuthModal  from '../components/auth-module';
import Input from '@/components/Input/Input';
import Button from '@/components/Button/Button';
import Register from '@/app/(auth)/api/api';
import axios from "axios";


export default function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const response = await Register {
                username,
                password,
                confirmPassword,
                email,
            });
            console.log("Success", response.data);
            navigate("/login");
        }
        catch (err) {
            if(axios.isAxiosError(err) && err.response) {
                const errorMsg = Object.values(err.response.data).flat().join(" ");
                setError(errorMsg);
            }
        }
  };

  const handleSignUp = (e: React.FormEvent) => {
    e.preventDefault();
    console.log();
  }
  return (
  <>  
    <AuthModal>
    <div className='text-center'>
      <h2 className="text-2xl font-semibold mb-6">Create an account</h2>
    </div>
    <div className='w-full max-w-sm mx-auto'>
      <form onSubmit={handleSignUp}>
      <p>User name</p>
      <Input 
        type="text"
        placeholder=""
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <p>Email address</p>
      <Input 
          type="email" 
          placeholder=""
          value={email}
          onChange={(e) => setEmail(e.target.value)}
      />
      <p>Password</p>
      <Input 
          type="password" 
          placeholder=""
          value={password}
          onChange={(e) => setPassword(e.target.value)}
      />
      <p>Confirm password</p>
      <Input 
          type="password" 
          placeholder=""
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
      />
      
      <div className="flex justify-center mt-6 mb-0.5">
        <Button className='text-xl w-full'>
          Create an account
        </Button>
      </div>
      
    </form>
    <div className='text-center'>
      <p>
        Already have an account? <a href="/login" className='underline'>Log in</a>
      </p>
    </div>
    </div>
    
    
    </AuthModal>
  </>
  );
};
