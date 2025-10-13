'use client'

import Layout from "@/app/components/Layout";
import React, { useState, useEffect } from "react";
import { fetchUserProfile } from "@/app/api/profile";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import Input from "@/app/components/Input"
import Button from "@/app/components/Button";
import {ProfileUpdatePayload, updateProfile} from "@/app/api/auth/update-profile";

interface UserProfile {
    first_name?: string;
    last_name?: string;
    birth_date: string; // В формате YYYY-MM-DD
    language?: string;
    language_level?: string;
    email: string;
    phone_number?: string;
    username: string;
}
type ProfileFormData = Omit<UserProfile, 'email'> & {
    email: string;
};

const toDateInput = (val?: string | null) =>
    val ? String(val).slice(0, 10) : "";

export default function Profile() {
    const [user, setUser] = useState<UserProfile | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const router = useRouter();

    const {
        register,
        handleSubmit,
        reset, // ⬅️ Для инициализации формы данными
        formState: { errors, isDirty } // ⬅️ isDirty для активации кнопки Save
    } = useForm<ProfileFormData>({
        defaultValues: {
            first_name: "",
            last_name: "",
            birth_date: "",
            language: "",
            language_level: "",
            phone_number: "",
            email: "",
            username: ""  // не используется в форме, но тип общий
        }
    });



    useEffect(() => {
        (async () => {
            try {
                const profileData = await fetchUserProfile();

                // нормализуем дату и забиваем форму
                const normalized: ProfileFormData = {
                    ...profileData,
                    birth_date: toDateInput(profileData?.birth_date),email: profileData.email,
                    phone_number: profileData?.phone_number || ''
                } as ProfileFormData;

                setUser(profileData);
                reset(normalized); //
                setError(null);
            } catch (err) {
                const message = err instanceof Error ? err.message : 'Failed to load profile';
                setError(message);
                console.error("Profile load failed:", message);
            } finally {
                setIsLoading(false);
            }
        })();
    }, [reset, router]);

    const onSubmit = async (data: ProfileFormData) => {
        setIsSaving(true);
        setError(null);
        setSuccessMessage(null);

        try {
            const payload: ProfileUpdatePayload = {};
            if (data.first_name && data.first_name.trim() !== '') {
                payload.first_name = data.first_name.trim();
            }

            if (data.last_name && data.last_name.trim() !== '') {
                payload.last_name = data.last_name.trim();
            }

            if (data.birth_date && data.birth_date.trim() !== '') {
                payload.birth_date = data.birth_date;
            }

            if (data.phone_number && data.phone_number.trim() !== '') {
                payload.phone_number = data.phone_number.trim();
            }

            if (data.language && data.language.trim() !== '') {
                payload.language = data.language.trim();
            }

            if (data.language_level && data.language_level.trim() !== '') {
                payload.language_level = data.language_level.trim();
            }

            // Если ничего не изменилось, не отправляем запрос
            if (Object.keys(payload).length === 0) {
                setError('No changes to save');
                setIsSaving(false);
                return;
            }

            const updated = await updateProfile(payload);

            const merged: UserProfile ={
                ...(user || ({} as UserProfile)),
                ...updated,
                email: user?.email || updated?.email,
                username: user?.username || updated?.username,
                birth_date: updated?.birth_date ? toDateInput(updated.birth_date): toDateInput(user?.birth_date),
            }

            setSuccessMessage('Profile successfully updated!');

            setUser(merged);
            reset({
                ...merged,
                birth_date: toDateInput(merged.birth_date),
                email: merged.email,
            } as ProfileFormData);
            setTimeout(() => setSuccessMessage(null), 1000);
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Failed to update profile';
            setError(message);
            console.error("Profile load failed:", message);
        } finally {
            setIsSaving(false);
        }
    };

    if (isLoading) {
        return (
            <Layout>
                <div className="text-center p-10">Загрузка профиля...</div>
            </Layout>
        );
    }


    return (
        <Layout>
            <div className="h-screen flex items-center justify-center p-4">
                <div className="bg-white p-12 rounded-3xl shadow-xl border border-gray-100
          w-full
          max-w-3xl lg:max-w-5xl xl:max-w-6xl 2xl:max-w-7xl
          max-h-[95vh] overflow-y-auto mx-auto flex flex-col">

                    <form
                        onSubmit={handleSubmit(onSubmit)}
                        className="bg-white p-4 md:p-8 rounded-xl max-w-5xl mx-auto w-full"
                    >

                        <div className="flex justify-between items-center mb-10">
                            <h1 className="text-3xl font-bold">Профиль</h1>
                            <Button
                                type='submit'
                                className={`text-[16px] font-medium py-2 px-6`}
                                disabled={!isDirty || isSaving} // ⬅️ Активируем кнопку только при изменении
                            >
                                {isSaving ? 'Сохранение...' : 'Save'}
                            </Button>
                        </div>

                        {error && (
                            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                                <p className="text-red-600 text-sm font-medium">
                                    {error}
                                </p>
                            </div>
                        )}

                        {successMessage && (
                            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                                <p className="text-green-600 text-sm font-medium">
                                    {successMessage}
                                </p>
                            </div>
                        )}

                        <div className="flex items-center space-x-4 mb-10 border-b pb-6">
                            <div className="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center text-3xl">
                                {user?.username ? user.username[0].toUpperCase() : 'U'}
                            </div>
                            <div>
                                {/* Имя пользователя (не редактируется) */}
                                <p className="text-xl font-semibold">{user?.username}</p>
                                {/* Email (поле ниже будет для отображения/редактирования) */}
                                <p className="text-gray-500">{user?.email}</p>
                            </div>
                        </div>

                        {/* Сетка полей ввода */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
                            {/* 1. First Name */}
                            <div>
                                <p className="text-gray-500 mb-1">First Name</p>
                                <Input
                                    type="text"
                                    {...register('first_name')}
                                    error={errors.first_name?.message}
                                />
                            </div>

                            {/* 2. Last Name */}
                            <div>
                                <p className="text-gray-500 mb-1">Last Name</p>
                                <Input
                                    type="text"
                                    {...register('last_name')}
                                    error={errors.last_name?.message}
                                />
                            </div>

                            {/* 3. Birth Date */}
                            <div>
                                <p className="text-gray-500 mb-1">Birth Date</p>
                                <Input
                                    type="date"
                                    {...register('birth_date')}
                                    error={errors.birth_date?.message}
                                />
                            </div>

                            {/* 4. Phone Number */}
                            <div>
                                <p className="text-gray-500 mb-1">Phone Number</p>
                                <Input
                                    type="tel"
                                    {...register('phone_number')}
                                    error={errors.phone_number?.message}
                                />
                            </div>

                            {/* 5. Language (Используем Input для простоты, в реальном проекте - Select) */}
                            <div>
                                <p className="text-gray-500 mb-1">Language</p>
                                {/* Тут в идеале должен быть Select с выпадающим списком */}
                                <Input
                                    type="text"
                                    {...register('language')}
                                    error={errors.language?.message}
                                />
                            </div>

                            {/* 6. Email (Не редактируется, но отображается как поле) */}
                            <div>
                                <p className="text-gray-500 mb-1">Email</p>
                                <Input
                                    type="email"
                                    disabled={true} // ⬅️ Делаем поле неактивным
                                    {...register('email')}
                                    error={errors.email?.message}
                                />
                            </div>

                            {/* 7. Language Level */}
                            <div>
                                <p className="text-gray-500 mb-1">Language level</p>
                                <Input
                                    type="text"
                                    {...register('language_level')}
                                    error={errors.language_level?.message}
                                />
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </Layout>
    );
}