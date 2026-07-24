import { Navigate, Route, Routes } from "react-router-dom";
import AuthLayout from "./components/AuthLayout";
import ProtectedLayout from "./components/ProtectedLayout";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import WorldDashboard from "./pages/WorldDashboard";
import Worlds from "./pages/Worlds";
import { useAuthStore } from "./store/auth";

export default function App() {
  const token = useAuthStore((state) => state.token);

  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path="/login" element={token ? <Navigate to="/" replace /> : <Login />} />
        <Route path="/register" element={token ? <Navigate to="/" replace /> : <Register />} />
      </Route>
      <Route element={<ProtectedLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/worlds" element={<Worlds />} />
        <Route path="/worlds/:worldId" element={<WorldDashboard />} />
      </Route>
      <Route path="*" element={<Navigate to={token ? "/" : "/login"} replace />} />
    </Routes>
  );
}
