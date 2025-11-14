"use client";
import React from "react";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import type { ProfileFormData } from "@/app/types/profile";
import Input from "@/app/components/Input";
import Button from "@/app/components/Button";
import { logout } from "@/app/lib/utils";

type Props = {
    profile: { username: string; email: string };
    initial: ProfileFormData;
    saving: boolean;
    error: string | null;
    success: string | null;
    onSubmit: (data: ProfileFormData) => Promise<unknown>;
};

const ProfileForm: React.FC<Props> = ({ profile, initial, saving, error, success, onSubmit }) => {
    const router = useRouter();
    const { register, handleSubmit, reset, formState: { errors, isDirty } } =
        useForm<ProfileFormData>({ defaultValues: initial });

    React.useEffect(() => { reset(initial, { keepDirty: false }); }, [initial, reset]);

    const handleLogout = () => {
        logout();
        // Используем window.location для полного редиректа и очистки состояния
        window.location.href = '/';
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="w-full">
            {/* Top section: Avatar + User Info + Save button */}
            <div className="flex items-start justify-between mb-10">
                {/* Left side: Avatar and user info */}
                <div className="flex items-center gap-5">
                    <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center text-3xl">
                        <span role="img" aria-label="avatar">😊</span>
                    </div>
                    <div>
                        <h2 className="text-2xl font-semibold text-gray-800">{profile.username}</h2>
                        <p className="text-gray-500 text-base">{profile.email}</p>
                    </div>
                </div>

                {/* Right side: Save button */}
                <Button
                    type="submit"
                    className="!w-auto !px-8 !py-3 bg-slate-700 hover:bg-slate-800 text-white rounded-lg shadow-md transition-colors text-base font-medium"
                    disabled={!isDirty || saving}
                >
                    {saving ? "Saving..." : "Save"}
                </Button>
            </div>

            {/* Error/Success messages */}
            {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-red-600 text-sm font-medium">{error}</p>
                </div>
            )}
            {success && (
                <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <p className="text-green-600 text-sm font-medium">{success}</p>
                </div>
            )}

            {/* Form fields - две колонки */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-8 mb-10">
                {/* Left column: First Name, Birth Date, Language */}
                <div>
                    <label className="block text-gray-700 text-base font-medium mb-3">First Name</label>
                    <Input 
                        type="text" 
                        {...register("first_name")} 
                        error={errors.first_name?.message}
                        size="md"
                        className="bg-gray-100"
                    />
                </div>
                <div>
                    <label className="block text-gray-700 text-base font-medium mb-3">Last Name</label>
                    <Input 
                        type="text" 
                        {...register("last_name")} 
                        error={errors.last_name?.message}
                        size="md"
                        className="bg-gray-100"
                    />
                </div>
                <div>
                    <label className="block text-gray-700 text-base font-medium mb-3">Birth Date</label>
                    <div className="relative">
                        <Input 
                            type="date" 
                            {...register("birth_date")} 
                            error={errors.birth_date?.message}
                            size="md"
                            className="bg-gray-100 pr-10"
                        />
                        <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                    </div>
                </div>
                <div>
                    <label className="block text-gray-700 text-base font-medium mb-3">Phone Number</label>
                    <Input 
                        type="tel" 
                        {...register("phone_number")} 
                        error={errors.phone_number?.message}
                        size="md"
                        className="bg-gray-100"
                    />
                </div>
                <div>
                    <label className="block text-gray-700 text-base font-medium mb-3">Language</label>
                    <div className="relative">
                        <Input
                            type="text"
                            placeholder="Select a language"
                            {...register("language")}
                            error={errors.language?.message}
                            size="md"
                            className="bg-gray-100 pr-10"
                        />
                        <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                    </div>
                </div>
                <div>
                    <label className="block text-gray-700 text-base font-medium mb-3">Email</label>
                    <Input 
                        type="email" 
                        disabled 
                        {...register("email")} 
                        error={errors.email?.message} 
                        value={profile.email}
                        size="md"
                        className="bg-gray-100"
                    />
                </div>
            </div>

            {/* Log out button - внизу слева */}
            <div className="mt-8">
                <button
                    type="button"
                    onClick={handleLogout}
                    className="px-6 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg border border-gray-300 transition-colors"
                >
                    Log out
                </button>
            </div>
        </form>
    );
};

export default ProfileForm;