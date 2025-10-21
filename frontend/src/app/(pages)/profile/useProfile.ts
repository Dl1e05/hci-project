"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { UserProfile, ProfileFormData } from "@/app/types/profile";
import { fetchUserProfile } from "@/app/api/profile";
import { updateProfile } from "@/app/api/auth/update-profile";
import { buildUpdatePayload, mergeProfiles, toFormData } from "./mappers";

export const useProfile = () => {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    // refs для таймеров, чтобы убирать предыдущие
    const errTimerRef = useRef<number | null>(null);
    const okTimerRef = useRef<number | null>(null);

    useEffect(() => {
        (async () => {
            try {
                const p = await fetchUserProfile();
                setProfile(p);
                setError(null);
            } catch (e) {
                const msg = e instanceof Error ? e.message : "Failed to load profile";
                setError(msg);
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    // авто-скрытие error (через 4 сек)
    useEffect(() => {
        if (!error) return;
        if (errTimerRef.current) window.clearTimeout(errTimerRef.current);
        errTimerRef.current = window.setTimeout(() => setError(null), 4000);
        return () => {
            if (errTimerRef.current) window.clearTimeout(errTimerRef.current);
        };
    }, [error]);

    // авто-скрытие success (через 2 сек)
    useEffect(() => {
        if (!success) return;
        if (okTimerRef.current) window.clearTimeout(okTimerRef.current);
        okTimerRef.current = window.setTimeout(() => setSuccess(null), 2000);
        return () => {
            if (okTimerRef.current) window.clearTimeout(okTimerRef.current);
        };
    }, [success]);

    const submit = useCallback(async (form: ProfileFormData) => {
        setSaving(true);
        setError(null);
        setSuccess(null);
        try {
            const payload = buildUpdatePayload(form);
            if (Object.keys(payload).length === 0) {
                setError("No changes to save");
                return null;
            }
            const updated = await updateProfile(payload);
            setProfile(prev => (prev ? mergeProfiles(prev, updated) : updated));
            setSuccess("Profile successfully updated!");
            return updated;
        } catch (e) {
            const msg = e instanceof Error ? e.message : "Failed to update profile";
            setError(msg);
            return null;
        } finally {
            setSaving(false);
        }
    }, []);

    const dismissError = () => setError(null);
    const dismissSuccess = () => setSuccess(null);

    return {
        profile,
        loading,
        saving,
        error,
        success,
        initialForm: profile ? toFormData(profile) : null,
        submit,
        dismissError,
        dismissSuccess,
    };
};
