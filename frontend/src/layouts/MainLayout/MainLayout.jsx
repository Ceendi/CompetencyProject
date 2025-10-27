import { Outlet } from "react-router-dom";
import "./MainLayout.css";
import Navbar from "../../components/Navbar/Navbar.jsx";
import InteractiveGridPattern from "../../components/InteractiveGridPattern/InteractiveGridPattern.jsx";

export default function MainLayout() {
  return (
    <div className="main-layout-container">
      <InteractiveGridPattern />
      <Navbar />
      <main className="main-layout-content">
        <Outlet />
      </main>
    </div>
  );
}
