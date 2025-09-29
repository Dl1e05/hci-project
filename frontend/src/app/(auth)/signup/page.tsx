'use client'
import React, { useState, useEffect } from 'react';
import AuthModal  from '../components/auth-module';
import Input from '@/components/Input/Input';
import Button from '@/components/Button/Button';
import Register from '@/app/(auth)/api/api';
import axios from "axios";

import { register } from '../api/register';
import axios from "axios";
import { useRouter } from 'next/navigation';


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

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        if (!email || !password || !confirmPassword || !username){
          setError('Пожалуйста, заполните все поля.')
        return;
        }
        if (password !== confirmPassword){
          setError("Пароли не совпадают")
          return;
        }
        setIsLoading(true);

        try {
            const response = await register({
                username,
                password,
                confirmPassword, //confirm_password: confirmPassword, // Имя поля может зависеть от бэкенда
                email,
                phone_number: '',
            });
            console.log("Success", response.data);
            router.push("/login");
        }
        catch (err) {
          if(axios.isAxiosError(err) && err.response) {
            const errorData = err.response.data;
            let errorMsg = "Ошибка регистрации.";

            if (typeof errorData === 'object' && errorData !== null) {
              errorMsg = Object.values(errorData).flat().join(" ");
            } else if (typeof errorData === 'string') {
              errorMsg = errorData;
            } else if (err.message) {
              errorMsg = err.message;
            } 
          setError(errorMsg);
        } else {
          setError("Сетевая ошибка или проблема с сервером.")
        } 

    } finally{
      setIsLoading(false)
    }
  };


  return (
  <>  
    <AuthModal>
    <div className='text-center'>
      <h2 className="text-2xl font-semibold mb-6">Create an account</h2>
    </div>
    <div className='w-full max-w-sm mx-auto'>
      <form onSubmit={handleSubmit}>
        {error && (
          <p className='text-red-500 text-sm mb-2 text-center font-medium'>{error}</p>
        )}
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
        <Button 
        type='submit'
        className={`text-xl w-full py-3`}
        disabled={isLoading}
        >
          {isLoading ? 'Регистрация...' : 'Create an account'}
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
