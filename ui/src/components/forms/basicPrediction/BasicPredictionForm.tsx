import React, {useState} from "react";
import './BasicPredictionForm.css'
import useSelectRef from "../../../hooks/useSelectRef.ts";
import {useInput} from "../../../hooks/useInput.ts";
import {BasicPredictionFormProps, handleInputBlur, handleSubmit} from "../const.ts";
import {SelectField} from "../../shared/Select/Select.tsx";
import {InputField} from "../../shared/Input/Input.tsx";
import {PredictButton} from "../../shared/Button.tsx";


const BasicPredictionForm = ({ setter }: BasicPredictionFormProps) => {

    const [disabled, setDisabled] = useState<boolean>(false);

    const [
        selectRef,
        isTouched,
        provideSelectValue
    ] = useSelectRef<string, string>();

    const [
        inputRef,
        provideValue
    ] = useInput();

    const onSubmit = () => handleSubmit(
        setter,
        provideSelectValue,
        provideValue,
        setDisabled,
    );

    return (
        <form className="prediction-form" onSubmit={(e) => e.preventDefault()}>
            <div className="inputs-container">
                <SelectField selectRef={selectRef} isTouched={isTouched} />
                <InputField inputRef={inputRef} onBlur={handleInputBlur} />
            </div>
            <PredictButton disabled={disabled}  onClick={onSubmit} />
        </form>
    );
};

export default BasicPredictionForm;