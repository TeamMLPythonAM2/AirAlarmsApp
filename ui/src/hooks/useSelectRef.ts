import {useRef, useState} from "react";
import {CSSObjectWithLabel, SelectInstance} from "react-select";

export type SelectType<T, K> = SelectInstance<{ value: T; label: K }> | null;

const useSelectRef = <T, K>() => {
    const [isTouched, setIsTouched] = useState(false);
    const selectRef = useRef<SelectType<T, K>>(null);

    const handleSubmit = () => {
        if (!selectRef.current || !selectRef.current?.getValue().length) {
            setIsTouched(true);
            return;
        }
        setIsTouched(false);
        return selectRef.current.getValue()[0].value;
    }

    const clearSelect = () => {
        setIsTouched(false);
        // if (selectRef.current)
        selectRef.current?.clearValue();
    }

    return [selectRef, isTouched, handleSubmit, clearSelect] as const;
}

export const resolveIsTouched = (isTouched: boolean, baseStyle: any): any => (
    {...baseStyle, ...(isTouched ? touchedStyle : {})}
)

const touchedStyle = {
    control: (base: CSSObjectWithLabel) => ({
        ...base,
        backgroundColor: '#8A54AB',
        color: '#fff3f3',
        borderColor: '#f47d9a',
        boxShadow: '0 0 0 1px #f47d9a',
        '&:hover': {
            borderColor:'#f496ac',
        },
    })
}

export default useSelectRef;