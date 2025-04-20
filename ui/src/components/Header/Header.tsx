import './Header.css'
import {ROUTES, RouteType} from "./routes.ts";
import {useState} from "react";
import {Link, Location, useLocation} from "react-router";


const Header = () => {
    const location = useLocation();
    const [isToggled, setIsToggled] = useState(false);
    return <div className="header-wrapper">
        <header>
            <div className="logo">
                <img src="/logo.svg" alt="logo"/>
                <h2>Alarms Predictor</h2>
            </div>
            <nav>
                <img onClick={() => setIsToggled(prev => !prev)}
                     className={"burger-menu " + (isToggled ? "toggled" : "")}
                     src='/burger-menu.svg' alt="menu"/>
                <div  className="dropdown-content">
                    <ul className="dropdown-links">
                        <NavRoutes location={location}/>
                    </ul>
                </div>
            </nav>
        </header>
    </div>
}

const NavRoutes = ({location}: {location: Location}) => {
    return ROUTES.map((route: RouteType, index) => (
        <li key={index} className={location.pathname.endsWith(route.path) ? "active" : ""}>
            <Link to={route.path}>{route.label}</Link>
        </li>
    ))
}

export default Header;