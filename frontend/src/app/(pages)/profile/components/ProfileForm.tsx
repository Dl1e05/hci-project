"use client";
import React from "react";
import { useForm } from "react-hook-form";
import type { ProfileFormData } from "@/app/types/profile";
import Input from "@/app/components/Input";
import Button from "@/app/components/Button";

type Props = {
    profile: { username: string; email: string };
    initial: ProfileFormData;
    saving: boolean;
    error: string | null;
    success: string | null;
    onSubmit: (data: ProfileFormData) => Promise<unknown>;
};

const ProfileForm: React.FC<Props> = ({ profile, initial, saving, error, success, onSubmit }) => {
    const { register, handleSubmit, reset, formState: { errors, isDirty } } =
        useForm<ProfileFormData>({ defaultValues: initial });

    React.useEffect(() => { reset(initial, { keepDirty: false }); }, [initial, reset]);

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="w-full">
            {/* Top section: Avatar + User Info + Save button */}
            <div className="flex items-start justify-between mb-8 -mt-16">
                {/* Left side: Avatar and user info */}
                <div className="flex items-center gap-4">
                    <div className="w-20 h-20 bg-yellow-400 rounded-full flex items-center justify-center text-3xl font-bold text-gray-700 border-4 border-white shadow-lg mt-7">
                        {profile.username ? profile.username[0].toUpperCase() : "U"}
                    </div>
                    <div className="mt-10">
                        <h2 className="text-xl font-semibold text-gray-800">{profile.username}</h2>
                        <p className="text-gray-500 text-sm">{profile.email}</p>
                    </div>
                </div>

                {/* Right side: Save button */}
                <Button
                    type="submit"
                    className="!w-auto !px-8 !py-2.5 mt-10"
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

            {/* Form fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                <div>
                    <label className="block text-gray-500 text-sm mb-2">First Name</label>
                    <Input type="text" {...register("first_name")} error={errors.first_name?.message} />
                </div>
                <div>
                    <label className="block text-gray-500 text-sm mb-2">Last Name</label>
                    <Input type="text" {...register("last_name")} error={errors.last_name?.message} />
                </div>
                <div>
                    <label className="block text-gray-500 text-sm mb-2">Birth Date</label>
                    <Input type="date" {...register("birth_date")} error={errors.birth_date?.message} />
                </div>
                <div>
                    <label className="block text-gray-500 text-sm mb-2">Phone Number</label>
                    <Input type="tel" {...register("phone_number")} error={errors.phone_number?.message} />
                </div>
                <div>
                    <label className="block text-gray-500 text-sm mb-2">Language</label>
                    <Input
                        type="text"
                        placeholder="Select a language"
                        {...register("language")}
                        error={errors.language?.message}
                    />
                </div>
                <div>
                    <label className="block text-gray-500 text-sm mb-2">Email</label>
                    <Input type="email" disabled {...register("email")} error={errors.email?.message} />
                </div>
                <div className="md:col-span-2">
                    <label className="block text-gray-500 text-sm mb-2">Language level</label>
                    <Input type="text" {...register("language_level")} error={errors.language_level?.message} />
                </div>
            </div>
        </form>
    );
};

export default ProfileForm;