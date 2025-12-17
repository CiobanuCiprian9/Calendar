import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

function GoogleSuccessPage() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const userId = params.get("user_id");
    const token = params.get("access_token");

    if (userId && token) {
      localStorage.setItem("user_id", userId);
      localStorage.setItem("access_token", token);
      navigate("/calendar", { replace: true });
    } else {
      navigate("/", { replace: true });
    }
  }, [location.search, navigate]);

  return <div>Logging you in with Google...</div>;
}

export default GoogleSuccessPage;
