import React from "react";
import './BasicPredictionForm.css'
import {regionsToI18Options} from "../../UkraineMap/RegionsAPI.ts";
import Select, {CSSObjectWithLabel} from "react-select";
import useSelectRef, {resolveIsTouched} from "../../../hooks/useSelectRef.ts";
import {fetchData} from "./BasicPredictionFormAPI.ts";

const BasicPredictionForm = () => {
    const [
        selectRef,
        isTouched,
        provideSelectValue,
        clearSelect
    ] = useSelectRef<string, string>();

    return(
        <form className="prediction-form">
            <label htmlFor="basicSelect">Choose the desired region</label>
            <div className="inputs-container">
                <Select
                    inputId="basicSelect"
                    ref={selectRef}
                    options={regionsToI18Options}
                    placeholder="Not selected"
                    menuPortalTarget={document.body}
                    styles={
                        resolveIsTouched(isTouched, selectStyle)
                    }
                />
                {/*<input type="number" min={1} max={24}/>*/}
            </div>
            <button onClick={(e) =>
                handleSubmit(e, provideSelectValue, clearSelect)}>
                Predict
            </button>
        </form>
    )}

const handleSubmit = async (
    e: React.MouseEvent,
    selectValueProviderFn: () => string | undefined,
    clearSelect: () => any
) => {
    e.preventDefault();
    const region = selectValueProviderFn();
    fetchData(region)
        .then(() => clearSelect())
        .catch((error) => console.log(error));
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
    backgroundColor: "#8A54AB",
    color: "#fff3f3",
    minHeight: 38,
    height: 'auto',
    outline: "none",
    fontSize: "20px",
    boxShadow: 'none',
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