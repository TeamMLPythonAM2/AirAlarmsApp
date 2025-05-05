import {useState} from "react";
import './FollowingDayPredictionForm.css'
import useSelectRef from "../../../hooks/useSelectRef.ts";
import {BasicPredictionFormProps} from "../const.ts";
import {SelectField} from "../../shared/Select/Select.tsx";
import {PredictButton} from "../../shared/Button.tsx";
import {
    ErrorMessage,
    getAlarmsFromResponse,
    handleSubmit,
    HourlyAlarmsForDay,
    LoadingMessage
} from "./AlarmsForDaySubmit.tsx";
import {ForecastData} from "./AlarmsForDayAPI.ts";


const AlarmsForFollowingDayForm = ({}: BasicPredictionFormProps) => {

    const [
        disabled,
        setDisabled
    ] = useState<boolean>(false);

    const [
        forecastData,
        setForecastData
    ] = useState<ForecastData | undefined>();

    const [
        isError,
        setError
    ] = useState<boolean>(false);

    const [
        isLoading,
        setLoader
    ] = useState<boolean>(false);

    const [
        selectRef,
        isTouched,
        provideSelectValue
    ] = useSelectRef<string, string>();

    const onSubmit = () => handleSubmit(
        setLoader,
        setForecastData,
        setError,
        provideSelectValue,
        setDisabled
    );


    return (
        <div>
            <form className="day-prediction-form"
                  onSubmit={(e) => e.preventDefault()}>
                <div className="inputs-container">
                    <SelectField selectRef={selectRef} isTouched={isTouched} />
                </div>
                <PredictButton disabled={disabled}  onClick={onSubmit} />
            </form>

            <ResultsTable isLoading={isLoading} isError={isError} forecastData={forecastData}/>
        </div>
    );
};

type ResultsTableProps = {
    isLoading: boolean;
    isError: boolean;
    forecastData: ForecastData | undefined;
}

const ResultsTable = ({isLoading, isError, forecastData}: ResultsTableProps) => {
    if (isLoading) return <LoadingMessage/>;
    if (isError) return <ErrorMessage/>;
    if (!forecastData) return <div></div>;
    return <HourlyAlarmsForDay {...getAlarmsFromResponse(forecastData.prediction.regions_forecast[forecastData.city_address])}/>
}

export default AlarmsForFollowingDayForm;