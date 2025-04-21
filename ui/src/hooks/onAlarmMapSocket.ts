import {useEffect, useState} from "react";

const socket = new WebSocket('ws://127.0.0.1:8000/ws/current_alerts');

export const ALARMS_KEY = "ALARMS_REGIONS"
const SPECIAL_REGIONS = ["crimea", "luhanska"];

const onAlarmMapSocket = () => {
    const [
        alarmRegions,
        setAlarmRegions
    ] = useState<string[]>([]);

    useEffect(() => {
        fetchStorage(setAlarmRegions)
        setUpSocketEvents(setAlarmRegions)
    }, []);



    return [alarmRegions]
}

function fetchStorage(setAlarmRegions: (regions: string[]) => void) {
    const locationData = localStorage.getItem(ALARMS_KEY) || JSON.stringify(SPECIAL_REGIONS);
    const regions = JSON.parse(locationData);
    setAlarmRegions(regions);
}

function setUpSocketEvents(setAlarmRegions: (regions: string[]) => void){
    socket.onmessage = (event) => {
        console.log("received")
        const eventData = JSON.parse(event.data);
        const data: string[] = [...SPECIAL_REGIONS, ...eventData];

        localStorage.setItem(ALARMS_KEY, JSON.stringify(data));
        setAlarmRegions(data);
    }

    socket.onerror = () => {
        localStorage.clear()
        console.log("onAlarmMapSocket error")
    }

    socket.onclose = () => {
        localStorage.clear()
        console.log("onAlarmMapSocket closed")
    }
}

export default onAlarmMapSocket