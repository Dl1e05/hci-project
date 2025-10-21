'use client'

import Layout from "@/app/components/Layout";
import ProfileForm from "@/app/(pages)/profile/components/ProfileForm";
import {useProfile} from "@/app/(pages)/profile/useProfile";

export default function ProfilePage() {
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
            <div className="min-h-screen flex items-center justify-center p-4">
                <div className="bg-white rounded-3xl shadow-2xl w-full max-w-3xl lg:max-w-5xl xl:max-w-6xl 2xl:max-w-7xl overflow-visible">
                    {/* Gradient header */}
                    <div className="h-20 bg-gradient-to-r from-slate-600 to-slate-400 rounded-t-3xl mb-10"></div>

                    <div className="px-8 md:px-12 py-8">
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
        </Layout>
    );
}