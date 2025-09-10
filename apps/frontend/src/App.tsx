import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppLayout from "./components/layout/AppLayout";
import Home from "./pages/Home";
import ExternalAppPage from "./pages/ExternalAppPage";
import { appRoutes } from "./routes/appRoutes";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Home />} />
          {appRoutes
            .filter(r => r.path !== "/") // index handled
            .map(r => (
              <Route
                key={r.key}
                path={r.path}
                element={r.kind === "external" ? <ExternalAppPage /> : <Home />}
              />
            ))}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
