import { useEffect, useState } from "react";
import { myTasks, updateStatus } from "../api/tasks";
import { getProfile } from "../api/tasks";

export default function UserDashboard() {
  const [tasks, setTasks] = useState([]);
  const [user, setUser] = useState({});

  const load = async () => {
    try {
      const res = await myTasks();
      setTasks(res.data?.tasks || []);
    } catch (err) {
      setTasks([]);
    }
  };

  const loadProfile = async () => {
    try {
      const res = await getProfile();
      setUser(res.data);
    } catch (err) {
      setUser({});
    }
  };

  useEffect(() => {
    load();
    loadProfile();
  }, []);

  const total = tasks.length;
  const completed = tasks.filter(t => t.status === "Done").length;
  const inProgress = tasks.filter(t => t.status === "In Progress").length;
  const todo = tasks.filter(t => t.status === "Todo").length;

  return (
    <div className="container mt-4">
      <h2 className="mb-3">User Dashboard</h2>

      <div className="card p-3 mb-4">
        <h5>User Profile</h5>
        <p><b>Email:</b> {user.email || "N/A"}</p>
        <p><b>Department:</b> {user.department || "N/A"}</p>
        <p><b>Experience:</b> {user.experience || "N/A"}</p>
        <p><b>Location:</b> {user.location || "N/A"}</p>
      </div>

      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>Total</h5>
            <h4>{total}</h4>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>Todo</h5>
            <h4>{todo}</h4>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>In Progress</h5>
            <h4>{inProgress}</h4>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>Completed</h5>
            <h4>{completed}</h4>
          </div>
        </div>
      </div>

      {tasks.length === 0 ? (
        <p>No tasks assigned</p>
      ) : (
        tasks.map(t => {
          const dueDate = new Date(t.due_date);
          const today = new Date();
          const isOverdue = dueDate < today && t.status !== "Done";

          return (
            <div key={t.id} className="card mb-3 p-3">
              <h5>{t.title}</h5>

              <p><b>Description:</b> {t.description || "N/A"}</p>
              <p><b>Status:</b> {t.status}</p>
              <p><b>Priority:</b> {t.priority}</p>
              <p><b>Due Date:</b> {t.due_date}</p>

              {isOverdue && <p className="text-danger">Overdue</p>}

              <div>
                <button
                  className="btn btn-primary me-2"
                  onClick={() => updateStatus(t.id, "In Progress").then(load)}
                >
                  Start
                </button>

                <button
                  className="btn btn-success"
                  onClick={() => updateStatus(t.id, "Done").then(load)}
                >
                  Complete
                </button>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}
