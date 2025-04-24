import PredictionOptionItem, {PredictionOption} from "../components/PredictionItem/PredictionOption.tsx";
import BasicPredictionForm from "../components/forms/basicPrediction/BasicPredictionForm.tsx";
import React from "react";
import './pages.css'

const PREDICTION_OPTIONS: PredictionOption[] = [
    {label: "Alarm in the following day chance", FormComponent: BasicPredictionForm},
    {label: "Coming soon...", FormComponent: React.Fragment}
]

const PredictionOptions = () => {
    return <div className="grid">
        <div>
            <h1 className="align-left">Choose prediction:</h1>
            <div className="align-left predictions-table">
                {<PredictionOptionsList/>}
            </div>
        </div>
        <div className="prediction-result">
            <img src="/animated_sphere.svg" alt="Prediction result"/>
            <img className="holder" src="/holder.svg" alt="holder"/>
        </div>
    </div>
}

const PredictionOptionsList = () => {
    return PREDICTION_OPTIONS.map(
        (option, index) =>
            <PredictionOptionItem
                key={option.label + index}
                {...option}
            />
    )
}

export default PredictionOptions;