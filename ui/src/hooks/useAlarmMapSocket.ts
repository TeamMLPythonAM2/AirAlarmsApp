import {useEffect, useState} from "react";


export const ALARMS_KEY = "ALARMS_REGIONS"
export const SPECIAL_REGIONS = ["crimea", "luhanska"];

const useAlarmMapSocket = () => {
    const [
        alarmRegions,
        setAlarmRegions
    ] = useState<string[]>([]);

    const socket = new WebSocket('ws://127.0.0.1:8000/ws/current_alerts');

    useEffect(() => {
        fetchStorage(setAlarmRegions)
        setUpSocketEvents(socket, setAlarmRegions)
    }, []);



    return [alarmRegions]
}

function fetchStorage(setAlarmRegions: (regions: string[]) => void) {
    const locationData = localStorage.getItem(ALARMS_KEY) || JSON.stringify(SPECIAL_REGIONS);
    const regions = JSON.parse(locationData);
    setAlarmRegions(regions);
}

function setUpSocketEvents(socket: WebSocket, setAlarmRegions: (regions: string[]) => void){
    socket.onmessage = (event) => {
        console.log("received")
        const eventData = JSON.parse(event.data);
        const data: string[] = [...SPECIAL_REGIONS, ...eventData];

        localStorage.setItem(ALARMS_KEY, JSON.stringify(data));
        setAlarmRegions(data);
    }

    socket.onerror = () => {
        localStorage.clear()
        socket.close()
        setAlarmRegions(SPECIAL_REGIONS);
        console.log("useAlarmMapSocket error")
    }

    socket.onclose = () => {
        localStorage.clear()
        setAlarmRegions(SPECIAL_REGIONS);
        console.log("useAlarmMapSocket closed")
    }
}

export default useAlarmMapSocket