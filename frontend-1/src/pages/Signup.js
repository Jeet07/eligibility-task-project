import { useState } from "react";
import { signup } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    department: "",
    experience: "",
    location: "",
    role: ""
  });

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!form.email || !form.password || !form.department || !form.experience || !form.location || !form.role) {
      alert("Please fill all fields");
      return;
    }

    if (form.password.length < 4) {
      alert("Password must be at least 4 characters");
      return;
    }

    try {
      setLoading(true);

      await signup({
        ...form,
        experience: Number(form.experience)
      });

      alert("Signup successful");
      navigate("/");
    } catch (err) {
      alert("Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
      <div className="card p-4" style={{ width: "350px" }}>
        <h3 className="text-center mb-3">Signup</h3>

        <input
          className="form-control mb-3"
          placeholder="Email"
          value={form.email}
          onChange={(e)=>setForm({...form,email:e.target.value})}
        />

        <input
          type="password"
          className="form-control mb-3"
          placeholder="Password"
          value={form.password}
          onChange={(e)=>setForm({...form,password:e.target.value})}
        />

        <select
          className="form-control mb-3"
          value={form.role}
          onChange={(e)=>setForm({...form,role:e.target.value})}
        >
          <option value="">Select Role</option>
          <option value="Admin">Admin</option>
          <option value="Manager">Manager</option>
          <option value="User">User</option>
        </select>

        <select
          className="form-control mb-3"
          value={form.department}
          onChange={(e)=>setForm({...form,department:e.target.value})}
        >
          <option value="">Select Department</option>
          <option value="Finance">Finance</option>
          <option value="HR">HR</option>
          <option value="IT">IT</option>
          <option value="Operations">Operations</option>
        </select>

        <input
          type="number"
          className="form-control mb-3"
          placeholder="Experience"
          value={form.experience}
          onChange={(e)=>setForm({...form,experience:e.target.value})}
        />

        <input
          className="form-control mb-3"
          placeholder="Location"
          value={form.location}
          onChange={(e)=>setForm({...form,location:e.target.value})}
        />

        <button
          className="btn btn-primary w-100 mb-2"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Signing up..." : "Signup"}
        </button>

        <button
          className="btn btn-outline-secondary w-100"
          onClick={() => navigate("/")}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
}
