import API from "./axios";

export const myTasks = () => API.get("/my-eligible-tasks");
export const updateStatus = (id, status) => API.put(`/tasks/${id}/status?status=${status}`);
export const createTask = (data) => API.post("/tasks/", data);
export const getEligibleUsers = (id) => API.get(`/tasks/${id}/eligible-users`);
export const recompute = () => API.post("/tasks/recompute-eligibility");
export const getMyCreatedTasks = () => API.get("/my-created-tasks");
export const getProfile = () => API.get("/user/profile");
