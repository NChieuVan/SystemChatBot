
import { Navigate, Outlet, useLocation } from "react-router-dom";

export default function RequireAuth() {
  const location = useLocation();
  const authed = !!localStorage.getItem("token");
  if (!authed) return <Navigate to="/login" replace state={{ from: location }} />;
  return <Outlet />;
}
