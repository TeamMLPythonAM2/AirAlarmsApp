
type PredictButtonProps = {
    disabled?: boolean;
    onClick: () => void;
};

export const PredictButton = ({ disabled, onClick }: PredictButtonProps) => {
    return <button className={disabled ? "disabled" : ""} disabled={disabled} type="button" onClick={onClick}>
        Predict
    </button>
};
