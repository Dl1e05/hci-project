import { ProfileFormData, UserProfile, ProfileUpdatePayload } from "@/app/types/profile";

const toDateInput = (val?: string | null) =>
    val ? String(val).slice(0, 10) : "";

export const toFormData = (p: UserProfile): ProfileFormData => ({
    ...p,
    birth_date: toDateInput(p.birth_date),
    phone_number: p.phone_number ?? "",
    language: p.language ?? "",
    language_level: p.language_level ?? "",
});

export const mergeProfiles = (base: UserProfile, patch: Partial<UserProfile>): UserProfile => ({
    ...base,
    ...patch,
    email: base.email ?? patch.email!,
    username: base.username ?? patch.username!,
    birth_date: patch.birth_date ?? base.birth_date ?? null,
});

export const buildUpdatePayload = (data: ProfileFormData): ProfileUpdatePayload => {
    const payload: ProfileUpdatePayload = {};
    const set = (k: keyof ProfileUpdatePayload, v?: string) => {
        const s = v?.trim();
        if (s) payload[k] = s;
    };
    set("first_name", data.first_name);
    set("last_name", data.last_name);
    set("birth_date", data.birth_date);
    set("phone_number", data.phone_number);
    set("language", data.language);
    set("language_level", data.language_level);
    return payload;
};