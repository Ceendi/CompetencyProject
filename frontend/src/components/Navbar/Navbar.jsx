import { Link, NavLink, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import Logo from "../../assets/icon-logo.svg";
import "./Navbar.css";

export default function Navbar() {
  const location = useLocation();

  return (
    <header className="navbar-header-outer">
      <div className="navbar-header-inner">
        <Link to="/" className="navbar-logo-name">
          <img src={Logo} alt="Logo" className="navbar-logo" />
          <h1 className="navbar-name">Video-Sent</h1>
        </Link>
        <nav className="navbar-links">
          <NavLink to="/" className="navbar-link">
            Dashboard
            {location.pathname === "/" && (
              <motion.div
                className="navbar-underline"
                layoutId="underline"
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              />
            )}
          </NavLink>
          <NavLink to="/reviews" className="navbar-link">
            Reviews
            {location.pathname === "/reviews" && (
              <motion.div
                className="navbar-underline"
                layoutId="underline"
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              />
            )}
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
