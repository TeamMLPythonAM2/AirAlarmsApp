import Accordion from "../shared/Accordion/Accordion.tsx";
import {PredictionOptionForm} from "../forms/const.ts";
import {Dispatch} from "react";

export interface PredictionOptionItemProps {
    label: string;
    FormComponent?: PredictionOptionForm;
}

export interface PredictionOption {
    label: string;
    FormComponent?: PredictionOptionForm;
    setPrediction: Dispatch<any>
}

const PredictionOptionItem = (
    {
        label,
        FormComponent,
        setPrediction,
    }: PredictionOption) => {
    return <Accordion
        accordionHead={<h4><span>{label}</span></h4>}
        accordionBody={
            FormComponent
                ? <FormComponent setter={setPrediction}/>
                : <></>
        }
    />
}


export default PredictionOptionItem;
