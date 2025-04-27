import React, {Dispatch} from "react";
import './BasicPredictionForm.css'
import {regionsToI18Options} from "../../UkraineMap/RegionsAPI.ts";
import Select, {CSSObjectWithLabel} from "react-select";
import useSelectRef, {resolveIsTouched} from "../../../hooks/useSelectRef.ts";
import {fetchData} from "./BasicPredictionFormAPI.ts";
import {useInput} from "../../../hooks/useInput.ts";
import {BasicPredictionFormProps} from "../const.ts";
import dropdown from "./eye.svg"

export const LOADING_MESSAGE = "Wait...";

const BasicPredictionForm = ({setter}: BasicPredictionFormProps) => {
    const [
        selectRef,
        isTouched,
        provideSelectValue,
        clearSelect
    ] = useSelectRef<string, string>();
    const [
        inputRef,
        provideValue
    ] = useInput();

    return(
        <form className="prediction-form">
            <div className="inputs-container">
                <div className="input-container">
                    <label htmlFor="basicSelect">
                        <span>Choose the desired region </span>
                    </label>
                    <Select
                        inputId="basicSelect"
                        ref={selectRef}
                        options={regionsToI18Options}
                        placeholder="Not selected"
                        isSearchable={false}
                        menuPortalTarget={document.body}
                        components={
                            {
                                DropdownIndicator:() => <img src={dropdown} alt={"indicator"}/>,
                                IndicatorSeparator:() => null
                            }
                        }
                        styles={
                            resolveIsTouched(isTouched, selectStyle)
                        }
                    />
                </div>
                <div className="input-container">
                    <label htmlFor="basicSelect">
                        <span>Chose how far the prediction is</span>
                    </label>
                    <input
                           ref={inputRef}
                           type="number"
                           defaultValue={1}
                           onInput={(e) => handleInput(e)}
                           min={1} max={24}
                    />
                </div>
            </div>
            <button onClick={(e) =>
                handleSubmit(e, setter, provideSelectValue, provideValue, clearSelect)}>
                Predict
            </button>
        </form>
    )}

const handleSubmit = async (
    e: React.MouseEvent,
    setter: Dispatch<any>,
    selectValueProviderFn: () => string | undefined,
    inputValueProvideFn: () => string | undefined,
    clearSelect: () => any
) => {
    e.preventDefault();
    const region = selectValueProviderFn();
    const hour = inputValueProvideFn();

    if (region && hour)
        setter(LOADING_MESSAGE);

    await new Promise((resolve) => setTimeout(resolve, 600));

    await fetchData(region, hour)
        .then(
            (data) => {
                setter("");
                setTimeout(() => {
                    if (!data) return;
                    setter(data);
                    clearSelect();
                }, 900);
            }
        )
        .catch(
            (error) => {
                setter(`Stars didn't align, nothing were predicted`);
                console.log(error);
            }
        );
};


const handleInput= (e: React.FormEvent) => {
    const input = e.target as HTMLInputElement;
    const value = Number.parseInt(input.value);
    console.log(!value || value <= 0)

    if (value > 24)
        return input.value = '24';
    if (!value || value <= 0)
        return input.value = '1';

}

const selectStyle: any = {
  menuPortal: (base: CSSObjectWithLabel) => ({
    ...base,
    zIndex: 2,
  }),
  menu: (base: CSSObjectWithLabel) => ({
    ...base,
    backgroundColor: "#440668",
  }),
  control: (base: CSSObjectWithLabel) => ({
    ...base,
    background: `linear-gradient(180deg, #C277D8 0%, #8345AA 100%)`,
    color: "#fff3f3",
    minHeight: 38,
    height: 'auto',
    outline: "none",
    fontSize: "20px",
    boxShadow: 'none',
    maxWidth: '300px',
    borderRadius: '10px',
    padding: '0',
    border: 'none',
    cursor: 'pointer',
  }),
  valueContainer: (base: CSSObjectWithLabel) => ({
    ...base,
    padding: '0 8px',
    height: '38px',
    display: 'flex',
    alignItems: 'center',
  }),
  singleValue: (base: CSSObjectWithLabel) => ({
    ...base,
    color: '#fff3f3',
    display: 'flex',
    alignItems: 'center',
  }),
  placeholder: (base: CSSObjectWithLabel) => ({
    ...base,
    color: "#fff3f3",
    display: 'flex',
    alignItems: 'center',
  }),
  input: (base: CSSObjectWithLabel) => ({
    ...base,
    margin: 0,
    padding: 0,
    color: '#fff3f3',
    caretColor: '#fff3f3'
  }),
  option: (base: CSSObjectWithLabel, state: any) => ({
    ...base,
    backgroundColor: state.isFocused ? "#6f398f" : "#8A54AB",
    cursor: 'pointer',
    color: '#fff3f3',
  }),
};


export default BasicPredictionForm;