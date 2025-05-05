import PredictionOptionItem, {PredictionOptionItemProps} from "../../components/PredictionItem/PredictionOption.tsx";
import BasicPredictionForm from "../../components/forms/basicPrediction/BasicPredictionForm.tsx";
import React, {Dispatch, useState} from "react";
import {AccordionsContext} from "../../components/shared/Accordion/Accordion.tsx";
import sphere from "./animated_sphere.svg";
import holder from "./holder.svg";
import '../pages.css'
import {LOADING_MESSAGE} from "../../components/forms/const.ts";
import AlarmsForFollowingDayForm from "../../components/forms/alarmsFor24Hours/FollowingDayPredictionForm.tsx";

const PREDICTION_OPTIONS: PredictionOptionItemProps[] = [
    {
        label: "Alarm in the following day chance",
        FormComponent: BasicPredictionForm
    },
    {
        label: "Alarms for the next 24 hours for city",
        FormComponent: AlarmsForFollowingDayForm
    },
    {
        label: "Coming soon...",
    }
]


const PredictionOptions = () => {
    const [
        prediction,
        setPrediction
    ] = useState<string>("");
    
    return <div className="grid">
        <div>
            <h1 className="align-left">Choose prediction:</h1>
            <div className="align-left predictions-table">
                <AccordionsContext.Provider value={[]}>
                    <PredictionOptionsList setPrediction={setPrediction}/>
                </AccordionsContext.Provider>
            </div>
        </div>
        <PredictionSphere prediction={prediction}/>
    </div>
}

const PredictionSphere = ({prediction}: {prediction: string}) => {
   return <div className="prediction-result">
        <img src={sphere} alt="Prediction result"/>
        <img className="holder" src={holder} alt="holder"/>
        <div className={
            "prediction" + (prediction || prediction == LOADING_MESSAGE ? " shown" : "")}>
            {prediction}
        </div>
    </div>
}

const PredictionOptionsList = ({setPrediction}: { setPrediction: Dispatch<any> }) => {
    return PREDICTION_OPTIONS.map(
        (option, index) =>
            <PredictionOptionItem
                key={option.label + index}
                setPrediction={setPrediction}
                {...option}
            />
    )
}

export default PredictionOptions;