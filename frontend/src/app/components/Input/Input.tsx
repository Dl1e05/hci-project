'use client';

import React, {ChangeEvent, useState} from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";

interface InputProps {
  type: string;
  placeholder: string;
  value: string;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
}

export default function Input({ type, placeholder, value, onChange }: InputProps) {
  const [showPassword, setShowPassword] = useState(false)
  
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  }

  const inputType = type === 'password' && showPassword ? 'text' : type;
  return (
    <div className="relative w-full mb-3">
      <input
        type={inputType}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="border rounded-md px-4 h-[56px] w-full"
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
    </div>
  )
}
