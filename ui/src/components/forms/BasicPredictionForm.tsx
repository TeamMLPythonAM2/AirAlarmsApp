import React from "react";
import './BasicPredictionForm.css'

export type BasicPredictionFormProps = {}
export type formComponentProps = BasicPredictionFormProps;
export type PredictionOptionForm = (props: formComponentProps) => React.ReactNode;

const BasicPredictionForm = () => {

    return <form className="prediction-form">
        <input type="text"/>
    </form>
}

export default BasicPredictionForm;