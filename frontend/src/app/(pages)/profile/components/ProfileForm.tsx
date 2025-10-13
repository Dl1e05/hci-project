"use client";

import React from "react";
import { useForm } from "react-hook-form";
import { ProfileFormData } from "@/app/types";
import Input from "@/app/components/Input";
import Button from "@/app/components/Button";

type Props = {
    initial: ProfileFormData;
    saving: boolean;
    error: string | null;
    success: string | null;
    onSubmit: (data: ProfileFormData) => Promise<unknown>;
};

export const ProfileForm: React.FC<Props> = ({ initial, saving, error, success, onSubmit }) => {
    const { register, handleSubmit, reset, formState: { errors, isDirty } } = useForm<ProfileFormData>({
        defaultValues: initial,
    });

    // когда пропсы initial меняются (после успешного сейва) — перезаписываем форму и сбрасываем dirty
    React.useEffect(() => {
        reset(initial, { keepDirty: false, keepTouched: false });
    }, [initial, reset]);

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-4 md:p-8 rounded-xl max-w-5xl mx-auto w-full">
            <div className="flex justify-between items-center mb-10">
                <h1 className="text-3xl font-bold">Профиль</h1>
                <Button type="submit" className="text-[16px] font-medium py-2 px-6" disabled={!isDirty || saving}>
                    {saving ? "Сохранение..." : "Save"}
                </Button>
            </div>

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

            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
                <div>
                    <p className="text-gray-500 mb-1">First Name</p>
                    <Input type="text" {...register("first_name")} error={errors.first_name?.message} />
                </div>
                <div>
                    <p className="text-gray-500 mb-1">Last Name</p>
                    <Input type="text" {...register("last_name")} error={errors.last_name?.message} />
                </div>
                <div>
                    <p className="text-gray-500 mb-1">Birth Date</p>
                    <Input type="date" {...register("birth_date")} error={errors.birth_date?.message} />
                </div>
                <div>
                    <p className="text-gray-500 mb-1">Phone Number</p>
                    <Input type="tel" {...register("phone_number")} error={errors.phone_number?.message} />
                </div>
                <div>
                    <p className="text-gray-500 mb-1">Language</p>
                    <Input type="text" {...register("language")} error={errors.language?.message} />
                </div>
                <div>
                    <p className="text-gray-500 mb-1">Email</p>
                    <Input type="email" disabled {...register("email")} error={errors.email?.message} />
                </div>
                <div>
                    <p className="text-gray-500 mb-1">Language level</p>
                    <Input type="text" {...register("language_level")} error={errors.language_level?.message} />
                </div>
            </div>
        </form>
    );
};
