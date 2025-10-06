'use client';
import React from 'react';
import { useForm } from 'react-hook-form';
import AuthModal from '../components/Auth-module';
import Input from '@/app/components/Input';
import Button from '@/app/components/Button';
import { login } from '@/app/api/auth/login'; // единый API-слой
import { useRouter } from 'next/navigation';

type LoginForm = {
  username_or_email: string;
  password: string;
  remember?: boolean;
};

export default function Login() {
  const router = useRouter();

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({ defaultValues: { username_or_email: '', password: '', remember: false } });

  const onSubmit = async (data: LoginForm) => {
    try {
      const res = await login({ username_or_email: data.username_or_email, password: data.password });
      const { access_token, refresh_token } = res || {};

      const storage = data.remember ? localStorage : sessionStorage;
      if (access_token) storage.setItem('access_token', access_token);
      if (refresh_token) storage.setItem('refresh_token', refresh_token);

      router.push('/');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка входа. Проверьте данные.';
      setError('root', { type: 'server', message });
    }
  };

  return (
    <AuthModal>
      <div className="text-center">
        <h2 className="text-[32px] font-semibold mb-10">Log into your account</h2>
      </div>

      <div className="w-full max-w-[555px] mx-auto">
        <form className="flex flex-col gap-2" onSubmit={handleSubmit(onSubmit)}>
          {errors.root?.message && (
            <p className="text-red-500 text-sm mb-2 text-center font-medium">{errors.root.message}</p>
          )}

          <div>
            <p>Email address</p>
            <Input
              type="email"
              {...register('username_or_email', {
                required: 'Введите email или username',
                pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: 'Некорректный email' },
              })}
              error={errors.username_or_email?.message}
            />
          </div>

          <div>
            <p>Password</p>
            <Input
              type="password"
              {...register('password', {
                required: 'Введите пароль',
                minLength: { value: 6, message: 'Минимум 6 символов' },
              })}
              error={errors.password?.message}
            />
          </div>

          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center gap-2">
              <input type="checkbox" id="remember-me" {...register('remember')} />
              <label htmlFor="remember-me">Remember me</label>
            </div>
            <a href="/forgot-password" className="underline">Forgot your password?</a>
          </div>

          <div className="flex justify-center mt-6 mb-0.5">
            <Button type="submit" className="text-xl" disabled={isSubmitting}>
              {isSubmitting ? 'Вход...' : 'Log in'}
            </Button>
          </div>
        </form>

        <div className="text-center p-2">
          <p>Don’t have an account? <a href="/signup" className="underline">Sign up</a></p>
        </div>
      </div>
    </AuthModal>
  );
}
