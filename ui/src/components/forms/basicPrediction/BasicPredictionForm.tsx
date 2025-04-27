import React from "react";
import './BasicPredictionForm.css'
import useSelectRef from "../../../hooks/useSelectRef.ts";
import {useInput} from "../../../hooks/useInput.ts";
import {BasicPredictionFormProps, handleInputBlur, handleSubmit} from "../const.ts";
import {SelectField} from "../../shared/Select/Select.tsx";
import {InputField} from "../../shared/Input/Input.tsx";
import {PredictButton} from "../../shared/Button.tsx";


const BasicPredictionForm = ({ setter }: BasicPredictionFormProps) => {
    const [
        selectRef,
        isTouched,
        provideSelectValue,
        clearSelect
    ] = useSelectRef<string, string>();

    const [
        inputRef,
        provideValue,
        clearInput
    ] = useInput();

    const onSubmit = () => handleSubmit(
        setter,
        provideSelectValue,
        provideValue,
        clearSelect,
        clearInput
    );

    return (
        <form className="prediction-form" onSubmit={(e) => e.preventDefault()}>
            <div className="inputs-container">
                <SelectField selectRef={selectRef} isTouched={isTouched} />
                <InputField inputRef={inputRef} onBlur={handleInputBlur} />
            </div>
            <PredictButton onClick={onSubmit} />
        </form>
    );
};

export default BasicPredictionForm;