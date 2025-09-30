import api from "../../api";


type RegisterPayload = {
  username: string;
  password: string;
  confirmPassword: string;
  email: string;
};

export async function register(payload: RegisterPayload) {
  const { data } = await api.post("/users/register/", payload);
  return data;
}

