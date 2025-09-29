import api from "../../api";


type LoginPayload = {
  password: string;
  email: string;
};

export async function login(payload: LoginPayload) {
  const { data } = await api.post("/users/login/", payload);
  return data;
}

