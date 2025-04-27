import React, {Dispatch} from "react";

export type BasicPredictionFormProps = {
    setter: Dispatch<any>
}
export type formComponentProps = BasicPredictionFormProps;
export type PredictionOptionForm = (props: formComponentProps) => React.ReactNode;