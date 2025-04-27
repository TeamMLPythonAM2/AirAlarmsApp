export const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

export const clampHourValue = (value: number) => {
    if (value > 24) return 24;
    if (value < 1 || !value) return 1;
    return value;
};
