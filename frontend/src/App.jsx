import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout/MainLayout";
import DashboardPage from "./pages/DashboardPage/DashboardPage";
import ReviewsPage from "./pages/ReviewsPage/ReviewsPage";
import { ReviewDetailPage } from "./pages/ReviewDetailPage/ReviewDetailPage";
import { VideosProvider } from "./context/VideosContext";

function App() {
  return (
    <VideosProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="reviews" element={<ReviewsPage />} />
            <Route path="reviews/:id" element={<ReviewDetailPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </VideosProvider>
  );
}

export default App;
