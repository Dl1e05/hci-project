import Link from "next/link";

export default function Home() {
  return (
      <div className="min-h-screen grid place-items-center">
        <div className="flex flex-col items-center gap-4 text-center">
          <h1 className="text-3xl font-semibold">Welcome</h1>

          <Link href="/login" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">
            Go to login
          </Link>
        </div>
      </div>
      
  );
}
