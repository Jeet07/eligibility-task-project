import { jwtDecode } from "jwt-decode";

export const getRole = () => {
  const token = localStorage.getItem("token");
  if (!token) return null;
  return jwtDecode(token).role;
};
