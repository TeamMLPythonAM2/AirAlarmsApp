import {FormEvent, Ref} from "react";

type InputFieldProps = {
    inputRef: Ref<HTMLInputElement>;
    onBlur: (e: FormEvent<HTMLInputElement>) => void;
};

export const InputField = ({ inputRef, onBlur }: InputFieldProps) => (
    <div className="input-container">
        <label htmlFor="predictionHours">
            <span>Choose how far the prediction is</span>
        </label>
        <input
            id="predictionHours"
            ref={inputRef}
            type="number"
            defaultValue={1}
            onBlur={onBlur}
            min={1}
            max={24}
        />
    </div>
);
