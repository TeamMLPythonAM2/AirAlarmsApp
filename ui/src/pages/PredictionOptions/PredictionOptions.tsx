import PredictionOptionItem, {PredictionOptionItemProps} from "../../components/PredictionItem/PredictionOption.tsx";
import BasicPredictionForm, {LOADING_MESSAGE} from "../../components/forms/basicPrediction/BasicPredictionForm.tsx";
import React, {Dispatch, useState} from "react";
import sphere from "./animated_sphere.svg";
import holder from "./holder.svg";
import '../pages.css'

const PREDICTION_OPTIONS: PredictionOptionItemProps[] = [
    {
        label: "Alarm in the following day chance",
        FormComponent: BasicPredictionForm
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
                <PredictionOptionsList setPrediction={setPrediction}/>
            </div>
        </div>
        <div className="prediction-result">
            <img src={sphere} alt="Prediction result"/>
            <img className="holder" src={holder} alt="holder"/>
            <div className={
                "prediction" + (prediction || prediction == LOADING_MESSAGE ? " shown" : "")}>
                {prediction}
            </div>
        </div>
    </div>
}

const PredictionOptionsList = ({setPrediction}: {setPrediction: Dispatch<any> }) => {
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