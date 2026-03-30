import { Link, useNavigate } from "react-router-dom";
import { getRole } from "../utils/auth";

export default function Navbar() {
  const role = getRole();
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3">
      
      {/* Brand */}
      <Link className="navbar-brand" to="/">
        Task Manager
      </Link>

      {/* Toggle (mobile) */}
      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      {/* Links */}
      <div className="collapse navbar-collapse" id="navbarNav">
        
        {/* Left side */}
        <ul className="navbar-nav me-auto">
          <li className="nav-item">
            <Link className="nav-link" to="/">Home</Link>
          </li>

          {role === "User" && (
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard">Dashboard</Link>
            </li>
          )}

          {role === "Admin" && (
            <li className="nav-item">
              <Link className="nav-link" to="/admin">Admin</Link>
            </li>
          )}
        </ul>

        {/* Right side */}
        <div className="d-flex align-items-center">
          {role && (
            <>
              <span className="text-white me-3">
                Role: {role}
              </span>

              <button className="btn btn-outline-light" onClick={logout}>
                Logout
              </button>
            </>
          )}
        </div>

      </div>
    </nav>
  );
}
