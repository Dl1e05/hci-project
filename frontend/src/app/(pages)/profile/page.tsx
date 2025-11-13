'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from "@/app/components/Layout";
import ProfileForm from "@/app/(pages)/profile/components/ProfileForm";
import {useProfile} from "@/app/(pages)/profile/useProfile";
import { isAuthenticated } from "@/app/lib/utils";

export default function ProfilePage() {
    const router = useRouter();
    
    // Немедленная проверка авторизации - если не авторизован, сразу редиректим
    useEffect(() => {
        if (!isAuthenticated()) {
            router.replace('/login');
        }
    }, [router]);

    // Если не авторизован, не рендерим ничего (редирект уже в процессе)
    if (!isAuthenticated()) {
        return null;
    }

    const {profile, loading, error, success, saving, initialForm, submit} = useProfile();

    if (loading) {
        return (
            <Layout>
                <div className="text-center p-10">Загрузка профиля...</div>
            </Layout>
        );
    }
    if (!profile || !initialForm) {
        return (
            <Layout>
                <div className="text-center p-10">Не удалось загрузить профиль</div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <div className="min-h-[60vh] flex items-center justify-center">
                    <div className="bg-white rounded-3xl shadow-lg w-full max-w-6xl 2xl:max-w-7xl overflow-visible">
                        <div className="px-12 md:px-16 lg:px-20 py-12 md:py-16">
                            <ProfileForm
                                profile={profile}
                                initial={initialForm}
                                saving={saving}
                                error={error}
                                success={success}
                                onSubmit={submit}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
}