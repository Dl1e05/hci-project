'use client';

import React, { forwardRef, useId, useState } from 'react';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

type Size = 'sm' | 'md' | 'lg';
type Variant = 'soft' | 'outline';

export interface InputProps
	extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
	label?: string;
	error?: string;
	helperText?: string;
	size?: Size;
	variant?: Variant;
	containerClassName?: string;
	leftAdornment?: React.ReactNode;
	rightAdornment?: React.ReactNode;
}

const cn = (...classes: Array<string | false | undefined>) =>
	classes.filter(Boolean).join(' ');

const baseBySize: Record<Size, string> = {
	sm: 'h-10 text-sm px-3 rounded-lg',
	md: 'h-14 text-base px-4 rounded-xl',
	lg: 'h-16 text-base px-5 rounded-2xl',
};

const Input = forwardRef<HTMLInputElement, InputProps>(
	(
		{
			label,
			error,
			helperText,
			size = 'md',
			variant = 'soft',
			type = 'text',
			className,
			containerClassName,
			leftAdornment,
			rightAdornment,
			disabled,
			id,
			...props
		},
		ref
	) => {
		const autoId = useId();
		const inputId = id || autoId;
		const [showPassword, setShowPassword] = useState(false);

		const isPassword = type === 'password';
		const visualType = isPassword && showPassword ? 'text' : type;

		const variantClasses =
			variant === 'soft'
				? 'bg-slate-50 border border-slate-100 focus:bg-white focus:border-slate-300 focus:ring-2 focus:ring-slate-200'
				: 'bg-white border border-slate-300 focus:border-slate-400 focus:ring-2 focus:ring-slate-200';

		const errorClasses = error ? 'border-red-400 focus:border-red-500 focus:ring-red-200' : '';
		const disabledClasses = disabled ? 'opacity-60 cursor-not-allowed' : '';

		return (
			<div className={cn('w-full', containerClassName)}>
				{label && (
					<label htmlFor={inputId} className="mb-2 block text-slate-600">
						{label}
					</label>
				)}

				<div className="relative">
					{/* left adornment */}
					{leftAdornment && (
						<div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
							{leftAdornment}
						</div>
					)}

					<input
						id={inputId}
						ref={ref}
						type={visualType}
						disabled={disabled}
						className={cn(
							'w-full outline-none transition-colors',
							baseBySize[size],
							variantClasses,
							errorClasses,
							disabledClasses,
							leftAdornment ? 'pl-10' : '',
							// если будет кнопка/адорнмент справа — добавим отступ
							(rightAdornment || isPassword) ? 'pr-12' : '',
							'placeholder:text-slate-400 text-slate-800',
							className
						)}
						{...props}
					/>

					{/* password toggle OR right adornment */}
					{isPassword ? (
						<button
							type="button"
							onClick={() => setShowPassword(s => !s)}
							className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
							tabIndex={-1}
						>
							{showPassword ? <FaEyeSlash /> : <FaEye />}
						</button>
					) : rightAdornment ? (
						<div className="absolute right-3 top-1/2 -translate-y-1/2">{rightAdornment}</div>
					) : null}
				</div>

				{/* helper / error */}
				{error ? (
					<p className="mt-1.5 text-xs text-red-600">{error}</p>
				) : helperText ? (
					<p className="mt-1.5 text-xs text-slate-400">{helperText}</p>
				) : null}
			</div>
		);
	}
);

Input.displayName = 'Input';
export default Input;
