import './App.css'
import './pages/pages.css'
import {BrowserRouter, Navigate, Route, Routes} from "react-router";
import Header from "./components/Header/Header.tsx";
import {ROUTES, RouteType} from "./components/Header/routes.ts";
import Footer from "./components/Footer/Footer.tsx";

function App() {
  return (
    <main>
        <BrowserRouter>
            <Header/>
            <div className="content">
                <Routes>
                    {
                        ROUTES.map((route: RouteType) => (
                            <Route Component={route.component} path={route.path}/>
                        ))
                    }
                    <Route path="*" Component={() => <Navigate to='/'/>}/>
                </Routes>
            </div>
            <Footer/>
        </BrowserRouter>
    </main>
  )
}

export default App
