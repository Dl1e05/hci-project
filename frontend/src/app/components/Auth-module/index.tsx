import { ReactNode } from "react";

export default function AuthModal({children}: {children: ReactNode}){
    return (
       <div className="h-screen flex items-center justify-center p-4">
        <div className="bg-white p-6 rounded-[40px] shadow-lg border border-gray-300 
        w-full max-w-[800px] h-[730px]
        overflow-y-hidden flex flex-col items-center justify-center
        ">
        {children}
      </div>
    </div>
  );
}

