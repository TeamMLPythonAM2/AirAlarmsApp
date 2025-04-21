import UkraineMap from "../components/UkraineMap/UkraineMap.tsx";
import onAlarmMapSocket from "../hooks/onAlarmMapSocket.ts";


const Home = () => {
    return(
    <>
        <h1>Current alarms</h1>
        <UkraineMap/>
    </>
)}

export default Home;