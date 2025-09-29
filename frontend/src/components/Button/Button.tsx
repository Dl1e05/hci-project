'use client';
import React from "react";

interface ButtonProps{
    children: React.ReactNode;
    onClick?: () => void;
    type?: "button" | "submit" | "reset";
    className?: string
    disabled?: boolean
}



export default function Button({children, onClick, type = "button", className = "", disabled = false}: ButtonProps) {
  const baseStyles = "w-90 py-1.5 px-10 border border-gray-400 rounded-full font-semibold text-gray-700 hover:bg-gray-100 transition-colors duration-200"
  return (
    <button
      type = {type}
      onClick = {onClick}
      disabled = {disabled}
      className={`${baseStyles} ${className}`}
    >
      {children}
    </button>
  )
}
