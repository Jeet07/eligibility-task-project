import { useState, useEffect } from "react";
import { login } from "../api/auth";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      const decoded = jwtDecode(token);
      if (decoded.role === "Admin") {
        navigate("/admin");
      } else {
        navigate("/dashboard");
      }
    }
  }, []);

  const handleSubmit = async () => {
    if (!form.email || !form.password) {
      alert("Please enter email and password");
      return;
    }

    try {
      setLoading(true);

      const res = await login(form);
      const token = res.access_token;

      localStorage.setItem("token", token);

      const decoded = jwtDecode(token);

      if (decoded.role === "Admin") {
        navigate("/admin");
      } else {
        navigate("/dashboard");
      }

    } catch (err) {
      alert("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
      <div className="card p-4" style={{ width: "350px" }}>
        <h3 className="text-center mb-3">Login</h3>

        <input
          className="form-control mb-3"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          type="password"
          className="form-control mb-3"
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button
          className="btn btn-primary w-100 mb-2"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <button
          className="btn btn-outline-secondary w-100"
          onClick={() => navigate("/signup")}
        >
          Signup
        </button>
      </div>
    </div>
  );
}
