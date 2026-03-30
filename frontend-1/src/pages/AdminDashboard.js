import { useState, useEffect } from "react";
import { createTask, getEligibleUsers, recompute, getMyCreatedTasks } from "../api/tasks";

export default function AdminDashboard() {
  const [task, setTask] = useState({
    title: "",
    description: "",
    priority: "High",
    due_date: "",
    rules: { department: "", min_experience: 0, location: "", max_tasks: 5 }
  });

  const [taskId, setTaskId] = useState("");
  const [users, setUsers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [recomputing, setRecomputing] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const res = await getMyCreatedTasks();
    setTasks(res.data?.tasks || []);
  };

  const handleCreate = async () => {
    if (!task.title || !task.description || !task.due_date) {
      alert("Please fill all required fields");
      return;
    }

    if (!task.rules.department) {
      alert("Select department");
      return;
    }

    const formattedDate = new Date(task.due_date).toISOString();

    const payload = {
      ...task,
      rules: {
        department: task.rules.department,
        min_experience: Number(task.rules.min_experience || 0),
        location: task.rules.location,
        max_tasks: Number(task.rules.max_tasks || 5)
      },
      due_date: formattedDate
    };

    const res = await createTask(payload);

    if (res.data?.task_id) {
      setTaskId(res.data.task_id);
    }

    alert("Task Created");
    fetchTasks();
  };

  const fetchUsers = async () => {
    if (!taskId) {
      alert("Enter Task ID");
      return;
    }

    setLoadingUsers(true);

    const res = await getEligibleUsers(taskId);
    setUsers(res.data?.users || []);

    setLoadingUsers(false);
  };

  const handleRecompute = async () => {
    if (!taskId) {
      alert("Enter Task ID");
      return;
    }

    setRecomputing(true);

    await recompute();

    setTimeout(() => {
      fetchUsers();
      setRecomputing(false);
    }, 3000);
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Admin Dashboard</h2>

      <div className="card p-3 mb-4">
        <h4>Create Task</h4>

        <input className="form-control mb-2" placeholder="Title"
          onChange={(e)=>setTask({...task,title:e.target.value})} />

        <input className="form-control mb-2" placeholder="Description"
          onChange={(e)=>setTask({...task,description:e.target.value})} />

        <input type="datetime-local" className="form-control mb-2"
          onChange={(e)=>setTask({...task,due_date:e.target.value})} />

        <select className="form-control mb-2"
          onChange={(e)=>setTask({...task, rules:{...task.rules,department:e.target.value}})}>
          <option value="">Select Department</option>
          <option value="Finance">Finance</option>
          <option value="HR">HR</option>
          <option value="IT">IT</option>
          <option value="Operations">Operations</option>
        </select>

        <input type="number" className="form-control mb-2" placeholder="Min Experience"
          onChange={(e)=>setTask({...task, rules:{...task.rules,min_experience:e.target.value}})} />

        <input className="form-control mb-2" placeholder="Location"
          onChange={(e)=>setTask({...task, rules:{...task.rules,location:e.target.value}})} />


        <button className="btn btn-primary" onClick={handleCreate}>
          Create Task
        </button>
      </div>

      <div className="card p-3 mb-4">
        <h4>Created Tasks</h4>

        {tasks.length === 0 ? (
          <p>No tasks found</p>
        ) : (
          tasks.map(t => (
            <div key={t.id} className="border p-2 mb-2">
	      <b>{t.title}</b>
	      <p>Task Id: {t.id}</p>
              <p>Status: {t.status}</p>
              <p>Priority: {t.priority}</p>
              <p>Due Date: {t.due_date}</p>
              <p>Department: {t.rules?.department || "N/A"}</p>
              <p>Experience: {t.rules?.min_experience || "N/A"}</p>
              <p>Location: {t.rules?.location || "N/A"}</p>
              <p>Max Tasks: {t.rules?.max_tasks || "N/A"}</p>
            </div>
          ))
        )}
      </div>

      <div className="card p-3">
        <h4>Eligible Users</h4>

        <input
          className="form-control mb-2"
          placeholder="Task ID"
          value={taskId}
          onChange={(e)=>setTaskId(e.target.value)}
        />

        <div className="mb-2">
          <button className="btn btn-success me-2" onClick={fetchUsers}>
            Fetch Users
          </button>

          <button className="btn btn-warning" onClick={handleRecompute}>
            Recompute
          </button>
        </div>

        {loadingUsers && <p>Loading users...</p>}
        {recomputing && <p>Recomputing... please wait</p>}

        {users.length > 0 ? (
          users.map(u => (
            <div key={u.id} className="border p-2 mb-1">
              {u.email}
            </div>
          ))
        ) : (
          !loadingUsers && <p>No users found</p>
        )}
      </div>
    </div>
  );
}
