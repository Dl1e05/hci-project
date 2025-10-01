'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; 
import AuthModal from '../components/auth-module';
import Input from '@/app/components/Input/Input';
import { login } from '@/app/(auth)/api/login';
import Button from '@/app/components/Button/Button';
import axios from 'axios';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null)

    if (email == 'test@gmail.com' && password == 'qwerty'){
      router.push("/profile")
    }

    if (!email || !password){
      setError('Пожалуйста, заполните все поля.')
      return;
    }

    setIsLoading(true);

    try{
      const response = await login({email, password});
      console.log('Успешный вход: ', response);

      router.push("/")
    } catch (err){
      if (axios.isAxiosError(err) && err.response){
        // Логика для извлечения сообщений об ошибках от API
        const errorData = err.response.data;
        let errorMsg = "Ошибка входа. Проверьте учетные данные.";
        
        // Попытка извлечь осмысленное сообщение об ошибке
        if (typeof errorData === 'object' && errorData !== null) {
             errorMsg = Object.values(errorData).flat().join(" ");
        } else if (typeof errorData === 'string') {
             errorMsg = errorData;
        } else if (err.message) {
             errorMsg = err.message;
        }
        setError(errorMsg)
      } else {
        setError('Сетевая ошибка или проблема с сервером.')
      }
    } finally{
      setIsLoading(false)
    }
  }


  return (
  <>  
  <AuthModal>
    <div className='text-center'>
      <h2 className="text-[32px] font-semibold mb-10">Log into your account</h2>
    </div>
    
    <div className='w-full max-w-[555px] mx-auto'>
      <form className='flex flex-col gap-2' onSubmit={handleSubmit}>
        {error && (
              <p className="text-red-500 text-sm mb-2 text-center font-medium">{error}</p>
        )}
      <div>
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
      </div>
      
      <div className="flex justify-between items-center text-sm">
        <div className="flex items-center">
          <input 
            type="checkbox" 
            id="remember-me" 
            name="remember-me" 
          />
          <label htmlFor="remember-me">Remember me</label>
        </div>
        <div>
          <a href="/forgot-password" className='underline'>Forgot your password?</a>
        </div>
      </div>
      <div className="flex justify-center mt-6 mb-0.5">
        <Button 
          type='submit'
          className='text-xl'
          disabled={isLoading}
        >
          {isLoading ? 'Вход...' : 'Log in'}
        </Button>
      </div>         
    </form>
    
    
      <div className="text-center p-2">
        <p>
          Don’t have an account? <a href="/signup" className="underline">Sign up</a>
        </p>
      </div>
    </div>
  </AuthModal>
  </>
  );
};
