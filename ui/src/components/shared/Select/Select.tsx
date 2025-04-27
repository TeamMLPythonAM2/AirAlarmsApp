import {regionsToI18Options} from "../../UkraineMap/RegionsAPI.ts";
import Select, {CSSObjectWithLabel} from "react-select";
import dropdown from './eye.svg'
import {resolveIsTouched} from "../../../hooks/useSelectRef.ts";

type SelectFieldProps = {
    selectRef: React.Ref<any>;
    isTouched: boolean;
};

export const SelectField = ({ selectRef, isTouched }: SelectFieldProps) => (
    <div className="input-container">
        <label htmlFor="basicSelect">
            <span>Choose the desired region</span>
        </label>
        <Select
            inputId="basicSelect"
            ref={selectRef}
            options={regionsToI18Options}
            placeholder="Not selected"
            isSearchable={false}
            menuPortalTarget={document.body}
            components={{
                DropdownIndicator: () => <img src={dropdown} alt="indicator" />,
                IndicatorSeparator: () => null,
            }}
            styles={resolveIsTouched(isTouched, selectStyle)}
        />
    </div>
);

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
