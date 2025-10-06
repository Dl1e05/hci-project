'use client';

import React, {ChangeEvent, forwardRef, useState} from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";

interface InputProps {
  type: string;
  value?: string;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  name?: string
  error?: string
}

const Input = forwardRef<HTMLInputElement, InputProps>(
	({ type, value, onChange, name, error }, ref) => {
		const [showPassword, setShowPassword] = useState(false)

		const togglePasswordVisibility = () => {
			setShowPassword(!showPassword)
		}

		const inputType = type === 'password' && showPassword ? 'text' : type
		return (
			<div className="relative w-full mb-3">
				<input
					ref={ref}
					type={inputType}
					value={value}
					onChange={onChange}
					name={name}
					className={`border rounded-md px-4 h-[56px] w-full ${
						error ? 'border-red-500' : ''
					}`}
				/>
				{type === 'password' && (
					<button
						type="button"
						onClick={togglePasswordVisibility}
						className="absolute inset-y-0 right-0 flex items-center pr-3"
					>
						{showPassword ? <FaEyeSlash /> : <FaEye />}
					</button>
				)}
				{error && <p className="absolute text-red-500 text-sm mt-0.25">{error}</p>}
			</div>
		)
	}
)
Input.displayName = 'Input'

export default Input