'use client'
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import AuthModal  from '../components/Auth-module';
import Input from '@/app/components/Input';
import Button from '@/app/components/Button';
import { register } from '@/app/api/auth/register';
import { useRouter } from 'next/navigation';

interface SignUpFormData {
  username: string
  email: string
  birth_date: string
  password: string
  password_repeat: string
}

export default function SignUp() {
  const [isLoading, setIsLoading] = useState(false);

  const router = useRouter();

  const {
    register: registerField,
    handleSubmit,
    watch,
    setError,
    formState: { errors }
  } = useForm<SignUpFormData>()
  
  const password = watch('password')

  const onSubmit = async (data: SignUpFormData) => {
    setIsLoading(true)

    try {
      const response = await register({
        username: data.username,
        birth_date: data.birth_date,
        password: data.password,
        password_repeat: data.password_repeat,
        email: data.email
      })
      console.log('Success', response)
      router.push('/login')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Registration failed'
      setError('root', { type: 'server', message })
    } finally {
      setIsLoading(false)
    }
  }


  return (
    <>  
      <AuthModal>
        <div className='text-center'>
          <h2 className="text-[32px] font-semibold mb-6">Create an account</h2>
        </div>
      
        <div className='w-full max-w-[555px] mx-auto'>
          <form onSubmit={handleSubmit(onSubmit)}>
            {errors.root?.message && (
              <p className='text-red-500 text-sm mb-2 text-center font-medium'>
                {errors.root.message}
              </p>
            )}
            <div>
              <p>User name</p>
              <Input 
                type="text"
                {...registerField('username', {
                  required: 'Username is required',
                  minLength: {
                    value: 3,
                    message: 'Username must be at least 3 characters'
                  }
                })}
                error={errors.username?.message}
              />
            </div>
            
            <div>
              <p>Email address</p>
              <Input 
                type="email" 
                {...registerField('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address'
                  }
                })}
                error={errors.email?.message}
              />
            </div>

            <div>
              <p>Birth date</p>
              <Input 
                type="date"
                {...registerField('birth_date', {
                  required: 'birth date is required',
                })}
                error={errors.birth_date?.message}
              />
            </div>
            
            <div>
              <p>Password</p>
                <Input
                  type="password"
                  {...registerField('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 6,
                      message: 'Password must be at least 6 characters'
                    }
                  })}
                  error={errors.password?.message}
                />
            </div>
            <div>
              <p>Confirm password</p>
                <Input
                  type="password"
                  {...registerField('password_repeat', {
                    required: 'Please confirm your password',
                    validate: (value) =>
                      value === password || 'Passwords do not match'
                  })}
                  error={errors.password_repeat?.message}
                />
            </div>
          
            <div className="flex justify-center mt-6 mb-0.5">
              <Button 
                type='submit'
                className={`text-[22px] font-medium`}
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
