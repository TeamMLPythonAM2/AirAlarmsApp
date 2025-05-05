import {CSSProperties, Dispatch, memo} from "react";
import {sleep} from "../utils.ts";
import alarmBall from "./icons/alarm_ball.svg";
import clearBall from "./icons/clear_ball.svg";
import './FollowingDayPredictionForm.css'
import {AlarmsForDayPrediction, fetchData, ForecastData} from "./AlarmsForDayAPI.ts";

export const LoadingMessage = () => <MessageInfoItem message={"Predicting..."}/>
export const ErrorMessage = () => <MessageInfoItem message={"Stars didn't align, nothing was predicted"}/>

export type Alarm = {
    time: string,
    isAlarm: boolean
}

export type Props = {
    alarms: Alarm[]
}

export const HourlyAlarmsForDay = memo(
    ({alarms} : Props
) => {
    return <div className="container">
        {alarms.map((alarm: Alarm, index) => (
            <AlarmInfoItem key={alarm.time + index} alarm={alarm}/>
        ))}
    </div>
})

const container: CSSProperties = {
    display: "grid",
    margin: "10px 30px 30px 30px",
    padding: "10px",
    borderRadius: "25px",
    background: 'radial-gradient(50% 50% at 50% 50%, #4D2964 10%, #321F44 99.99%)',
    gridAutoFlow: "column",
    gridTemplateRows: "repeat(6, 1fr)"
}

const AlarmInfoItem = ({alarm} : {alarm: Alarm}) => {
    return <div style={alarmInfoItem}>
        <span>{alarm.time}</span>
        <img
            src={alarm.isAlarm ? alarmBall : clearBall}
            alt={alarm.isAlarm ? "Alarm" : "No Alarm"}
        />
    </div>
}

const alarmInfoItem: CSSProperties = {
    display: "flex",
    fontFamily: "'Aldrich', sans-serif",
    justifyContent: "center",
    gap: "15px",
    alignItems: "center",
}

const MessageInfoItem = ({message}: {message: string}) => {
    return <div style={messageInfoItem}>{message}</div>
}

const messageInfoItem: CSSProperties = {
    fontFamily: "'Aldrich', sans-serif",
    display: "flex",
    margin: "15px 0",
    justifyContent: "center"
}

export const getAlarmsFromResponse = (regions_forecast: { [time: string]: boolean }): Props => {
    const alarms = Object.entries(regions_forecast).map(
        ([time, isAlarm]): Alarm => ({
          time: time,
          isAlarm: isAlarm
        })
    )
    return {alarms: alarms};
}

export const handleSubmit = async (
    setLoader: Dispatch<boolean>,
    setData: Dispatch<ForecastData | undefined>,
    setError: Dispatch<boolean>,
    getSelectValue: () => string | undefined,
    toggleButton: Dispatch<any>,
) => {
    const region = getSelectValue();

    if (!region) return;
    setLoader(true);
    setError(false)
    toggleButton(true);

    try {
        await sleep(600);
        const data = await fetchData(region);

        if (!data?.prediction) return;
        console.log(data)
        setData(data);
    } catch (error) {
        setError(true)
        console.warn(error);
    } finally {
        setLoader(false);
    }
    toggleButton(false);
};

