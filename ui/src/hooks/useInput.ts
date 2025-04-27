import React, {useRef} from "react";


export const useInput = (): [
    React.Ref<HTMLInputElement>,
    () => string | undefined,
    () => void
] => {
    const inputRef = useRef<HTMLInputElement>(null);
    function provideInputValue(){
        return inputRef.current?.value;
    }

    function clearInputValue() {
        if (inputRef.current?.value)
            inputRef.current.value = '1';
        return;
    }
    return [inputRef, provideInputValue, clearInputValue] as const;
}