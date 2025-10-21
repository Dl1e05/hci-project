export interface UserProfile {
    first_name?: string;
    last_name?: string;
    birth_date: string; // В формате YYYY-MM-DD
    language?: string;
    language_level?: string;
    email: string;
    phone_number?: string;
    username: string;
}

export type ProfileFormData = Omit<UserProfile, 'email'> & {
    email: string;
};
export type ProfileUpdatePayload = Partial<{
    first_name: string;
    last_name: string;
    birth_date: string;
    language: string;
    language_level: string;
    phone_number: string;
}>;