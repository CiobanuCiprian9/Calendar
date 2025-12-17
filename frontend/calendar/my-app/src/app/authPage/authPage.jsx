import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./authPage.css";

const API_BASE = process.env.REACT_APP_API_ORIGIN || "http://localhost:8000";

function AuthPage() {
  const [tab, setTab] = useState("login");

  const [loginForm, setLoginForm] = useState({
    email: "",
    password: "",
  });

  const [registerForm, setRegisterForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate=useNavigate();

  const handleGoogle = () => {
    window.location.href = `${API_BASE}/auth/google/login`;
  };

  //login
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const{email,password}=loginForm;

    //data missing
    if(
      !email.trim() ||
      !password
    ) {
      setError("Email or password missing");
      return;
    }

    try{
      const res=await fetch(`${API_BASE}/auth/login`, {
        method:"POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if(!res.ok){
        const body=await res.json().catch(()=>null);

        if(body?.detail) {
          setError(body.detail);
        }else{
          setError("Login failed");
        }
        return;
      }

      const data = await res.json();
      localStorage.setItem("user_id", data.user_id);

      navigate("/calendar")
    }
    catch(err){
      console.error(err);
      setError("Server error");
    }
  };

  //register
  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const{first_name,last_name,email,password,confirm_password}=registerForm;

    //data missing
    if(
      !first_name.trim() ||
      !last_name.trim() ||
      !email.trim() ||
      !password ||
      !confirm_password
    ) {
      setError("All data is obligatory");
      return;
    }

    //confirm password
    if(password!==confirm_password) {
      setError("Confirm password is not the same as password");
      return;
    }

    try{
      const res=await fetch(`${API_BASE}/auth/register`, {
        method:"POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          first_name,
          last_name,
          email,
          password,
        }),
      });

      if(!res.ok) {
        const body=await res.json().catch(()=>null);

        if(body?.detail){
          setError(body.detail);
        } else {
          setError("Register failed");
        }
        return;
      }

      setSuccess("Register succesfully");
      setTab("login");

      setLoginForm({email,password:""});
    } catch (err) {
      console.error(err);
      setError("Server error");
    }
  };

  return (
    <div className="authPage">
      <div className="signin-container">
        {error && <div className="error-box">{error}</div>}
        {success && <div className="success-box">{success}</div>}

        <div className="tabs">
          <button
            className={tab === "login" ? "tab active" : "tab"}
            onClick={() => setTab("login")}
          >
            Login
          </button>
          <button
            className={tab === "register" ? "tab active" : "tab"}
            onClick={() => setTab("register")}
          >
            Register
          </button>
        </div>

        {tab === "login" && (
          <form className="auth-form" onSubmit={handleLoginSubmit}>
            <h1 className="title">Sign In</h1>

            <label className="field">
              <span>Email</span>
              <input
                type="email"
                value={loginForm.email}
                onChange={(e) =>
                  setLoginForm({ ...loginForm, email: e.target.value })
                }
              />
            </label>

            <label className="field">
              <span>Password</span>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) =>
                  setLoginForm({ ...loginForm, password: e.target.value })
                }
              />
            </label>

            <button className="primary-button" type="submit">
              Login
            </button>

            <div className="divider">or</div>

            <button
              className="google-button"
              type="button"
              onClick={handleGoogle}
            >
              <span id="google-text">Continue with Google</span>
            </button>
          </form>
        )}

        {tab === "register" && (
          <form className="auth-form" onSubmit={handleRegisterSubmit}>
            <h1 className="title">Register</h1>

            <label className="field">
              <span>First name</span>
              <input
                type="text"
                value={registerForm.first_name}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, first_name: e.target.value })
                }
              />
            </label>

            <label className="field">
              <span>Last name</span>
              <input
                type="text"
                value={registerForm.last_name}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, last_name: e.target.value })
                }
              />
            </label>

            <label className="field">
              <span>Email</span>
              <input
                type="email"
                value={registerForm.email}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, email: e.target.value })
                }
              />
            </label>

            <label className="field">
              <span>Password</span>
              <input
                type="password"
                value={registerForm.password}
                onChange={(e) =>
                  setRegisterForm({ ...registerForm, password: e.target.value })
                }
              />
            </label>

            <label className="field">
              <span>Confirm password</span>
              <input
                type="password"
                value={registerForm.confirm_password}
                onChange={(e) =>
                  setRegisterForm({
                    ...registerForm,
                    confirm_password: e.target.value,
                  })
                }
              />
            </label>

            <button className="primary-button" type="submit">
              Register
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default AuthPage;
