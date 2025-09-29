'use client';

import React, { useState } from 'react';
import AuthModal from '../components/auth-module';
import Input from '@/components/Input/Input';
import Button from '@/components/Button/Button';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  return (
  <>  
  <AuthModal>
    <div className='text-center'>
      <h2 className="text-2xl font-semibold mb-6">Log into your account</h2>
    </div>
    
    
    <div className='w-full max-w-sm mx-auto'>
      <form className='flex flex-col gap-2'>
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
      <div className="flex justify-between items-center text-sm">
        <div className="flex items-center">
          <input type="checkbox" id="remember-me" name="remember-me" />
          <label htmlFor="remember-me">Remember me</label>
        </div>
        <div>
          <a href="/forgot-password" className='underline'>Forgot your password?</a>
        </div>
      </div>
      <div className="flex justify-center mt-6 mb-0.5">
        <Button className='text-xl w-full'>
          Log in
        </Button>
      </div>         
    </form>
    
    
      <div className="text-center">
        <p>
          Don’t have an account? <a href="/signup" className="underline">Sign up</a>
        </p>
      </div>
    </div>
  </AuthModal>
  </>
  );
};
