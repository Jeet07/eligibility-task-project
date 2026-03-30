import { Navigate } from "react-router-dom";
import { getRole } from "../utils/auth";

export default function ProtectedRoute({ children, role }) {
  const userRole = getRole();
  if (!userRole) return <Navigate to="/" />;
  if (role && role !== userRole) return <h2>Access Denied</h2>;
  return children;
}
