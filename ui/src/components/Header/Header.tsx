import {ROUTES, RouteType} from "./routes.ts";
import {useState} from "react";
import React from "react";
import {Link, Location, useLocation} from "react-router";
import logoImage from "./logo.svg";
import burger from "./burger-menu.svg"


const Header = () => {
    const location = useLocation();
    const [isToggled, setIsToggled] = useState(false);

    return <div className="header-wrapper">
        <header>
            <div className="logo">
                <img src={logoImage} alt="logo"/>
                <div className="logo-img"></div>
                <h2>Alarms Predictor</h2>
            </div>
            <nav>
                <img onClick={() => setIsToggled(prev => !prev)}
                     className={"burger-menu " + (isToggled ? "toggled" : "")}
                     src={burger} alt="menu"/>

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