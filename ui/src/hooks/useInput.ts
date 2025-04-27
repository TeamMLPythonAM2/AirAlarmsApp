import React, {useRef} from "react";


export const useInput = (): [React.Ref<HTMLInputElement>, () => string | undefined] => {
    const inputRef = useRef<HTMLInputElement>(null);
    function provideInputValue(){
        return inputRef.current?.value;
    }
    return [inputRef, provideInputValue];
}