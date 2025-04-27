type PredictButtonProps = {
    onClick: () => void;
};

export const PredictButton = ({ onClick }: PredictButtonProps) => (
    <button type="button" onClick={onClick}>
        Predict
    </button>
);
