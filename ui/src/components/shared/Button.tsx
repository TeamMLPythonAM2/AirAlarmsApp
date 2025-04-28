
type PredictButtonProps = {
    disabled?: boolean;
    onClick: () => void;
};

export const PredictButton = ({ disabled, onClick }: PredictButtonProps) => {
    console.log(disabled)
    return <button disabled={disabled} type="button" onClick={onClick}>
        Predict
    </button>
};
