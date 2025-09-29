import { ReactNode } from "react";

export default function AuthModal({children}: {children: ReactNode}){
    return (
       <div className="h-screen flex items-center justify-center p-4">
        <div className="bg-white p-12 rounded-[40px] shadow-lg border border-gray-300 radius-
        w-full max-w-md sm:max-w-lg md:max-w-xl aspect-square max-h-[90vh] 
        overflow-y-hidden flex flex-col items-center justify-center
        ">
        {children}
      </div>
    </div>
  );
}

