'use client'

import Layout from "@/app/components/Layout";
// import Input from "@/app/components/Input";
import React from "react";
// import Button from "@/app/components/Button";
// import {useForm, FieldErrors} from "react-hook-form";
//
// type ProfileForm = {
//     username: string;
//     name: string;
//     last_name: string;
//     phone_number: string;
//     email: string;
//     password: string;
//     language: string;
//     language_level: string;
//     birth_date: string;
// };



export default function Profile() {
    // const {
    //     register,
    //     handleSubmit,
    //     formState: { errors, isSubmitting },
    // } = useForm<ProfileForm>({ defaultValues: { username:'',name: '', last_name: '', email: '', password: '', birth_date: '' } });
    //
    // const onSubmit = (data: ProfileForm) => {
    //     console.log('Profile data submitted:', data);
    // };
  return (
    <>
      <Layout>
          <div className="h-screen flex items-center justify-center p-4">
              <div className="bg-white p-12 rounded-3xl shadow-xl border border-gray-100
            w-full
            max-w-3xl      /* Базовая ширина для планшетов */
            lg:max-w-5xl   /* Ширина на 1024px+ (около 1024px) */
            xl:max-w-6xl   /* Ширина на 1280px+ (около 1152px) */
            2xl:max-w-7xl  /* Ширина на 1536px+ (около 1280px) */
            max-h-[95vh] overflow-y-auto
            mx-auto flex flex-col">
                  <div className="bg-white p-8 md:p-12 rounded-xl shadow-lg border border-gray-100 max-w-5xl mx-auto mt-10">

                      {/* 1. Блок Аватара, Имени и Кнопки Сохранения (Верхняя часть) */}
              {/*        <div className="flex justify-between items-center pb-8 border-b mb-6">*/}
              {/*            <div className="flex items-center gap-4">*/}
              {/*                <div>*/}
              {/*                    <h1 className="text-2xl font-semibold text-gray-800">username</h1>*/}
              {/*                    <p className="text-gray-500">email@gmail.com</p>*/}
              {/*                </div>*/}
              {/*            </div>*/}
              {/*            <button*/}
              {/*                type="submit" // Кнопка отправки формы*/}
              {/*                form="profile-form" // Связываем кнопку с формой ниже*/}
              {/*                disabled={isSubmitting}*/}
              {/*                className="bg-gray-700 text-white px-6 py-2 rounded-md hover:bg-gray-800 transition-colors disabled:opacity-60"*/}
              {/*            >*/}
              {/*                {isSubmitting ? 'Сохранение...' : 'Save'}*/}
              {/*            </button>*/}
              {/*        </div>*/}

              {/*        /!* 2. Основная Сетка Формы *!/*/}
              {/*        <form*/}
              {/*            id="profile-form"*/}
              {/*            onSubmit={handleSubmit(onSubmit)}*/}
              {/*            className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6"*/}
              {/*            noValidate*/}
              {/*        >*/}
              {/*            /!* 1-й ряд: First Name / Last Name *!/*/}
              {/*            <ProfileField label="First Name" name="name" errors={errors}>*/}
              {/*                <Input type="text" {...register('name')} />*/}
              {/*            </ProfileField>*/}
              {/*            <ProfileField label="Last Name" name="last_name" errors={errors}>*/}
              {/*                <Input type="text" {...register('last_name')} />*/}
              {/*            </ProfileField>*/}

              {/*            /!* 2-й ряд: Birth Date / Phone Number *!/*/}
              {/*            <ProfileField label="Birth Date" name="birth_date" errors={errors}>*/}
              {/*                <Input*/}
              {/*                    type="date"*/}
              {/*                    {...register('birth_date', { required: 'birth date is required' })}*/}
              {/*                />*/}
              {/*            </ProfileField>*/}
              {/*            <ProfileField label="Phone Number" name="phone_number" errors={errors}>*/}
              {/*                <Input type="text" {...register('phone_number')} />*/}
              {/*            </ProfileField>*/}

              {/*            /!* 3-й ряд: Language / Email (Email делаем только для отображения) *!/*/}
              {/*            <ProfileField label="Language" name="language" errors={errors}>*/}
              {/*                /!* Для Language лучше использовать Select, но оставляю Input по вашему коду *!/*/}
              {/*                <Input type="text" {...register('language')} placeholder="Select a language" />*/}
              {/*            </ProfileField>*/}
              {/*            <ProfileField label="Email" name="email" errors={errors}>*/}
              {/*                <Input*/}
              {/*                    type="email"*/}
              {/*                    {...register('email')}*/}
              {/*                    disabled={false} // Поле email обычно нередактируемо*/}
              {/*                    className="bg-gray-100 cursor-not-allowed"*/}
              {/*                />*/}
              {/*            </ProfileField>*/}

              {/*            /!* 4-й ряд: Language level / Password *!/*/}
              {/*            <ProfileField label="Language level" name="language_level" errors={errors}>*/}
              {/*                <Input type="text" {...register('language_level')} />*/}
              {/*            </ProfileField>*/}
              {/*            <ProfileField label="Password" name="password" errors={errors}>*/}
              {/*                <Input*/}
              {/*                    type="password"*/}
              {/*                    {...register('password', {*/}
              {/*                        required: 'Password is required',*/}
              {/*                        minLength: { value: 6, message: 'Password must be at least 6 characters' }*/}
              {/*                    })}*/}
              {/*                />*/}
              {/*            </ProfileField>*/}

              {/*        </form>*/}
              {/*        /!* </CardContainer> *!/*/}
                  </div>
              </div>
          </div>
      </Layout>
    </>
  );
}

// interface ProfileFieldProps {
//     placeholder?: string; // Добавлен для устранения ошибки TS2322
//     disabled?: boolean;
//     label: string;
//     children: React.ReactNode;
//     name: keyof ProfileForm;
//     errors: FieldErrors<ProfileForm>;
// }
//
// // Этот компонент берет на себя отображение подписи и ошибки, делая форму чище
// const ProfileField: React.FC<ProfileFieldProps> = ({ label, children, name, errors }) => (
//     <div>
//         <p className="mb-2 font-medium text-gray-700">{label}</p>
//         {children}
//         {errors[name]?.message && (
//             <p className="text-red-500 text-sm mt-1">{errors[name]?.message}</p>
//         )}
//     </div>
// );