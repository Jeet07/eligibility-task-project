import API from "./axios";

export const signup = (data) => API.post("/signup", data);
export const login = async (data) => {
  const res = await API.post("/login", data);
  localStorage.setItem("token", res.data.access_token);
  return res.data;
};
