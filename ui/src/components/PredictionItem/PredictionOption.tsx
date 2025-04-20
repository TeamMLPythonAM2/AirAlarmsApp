import Accordion from "../shared/Accordion/Accordion.tsx";
import {PredictionOptionForm} from "../forms/BasicPredictionForm.tsx";

export interface PredictionOption {
    label: string;
    FormComponent: PredictionOptionForm;
}

const PredictionOptionItem = <T, >({label, FormComponent}: PredictionOption) => {
    return <Accordion
        accordionHead={<h4><span>{label}</span></h4>}
        accordionBody={<FormComponent/>}
    />
}


export default PredictionOptionItem;
