import React, {Dispatch} from "react";

export type BasicPredictionFormProps = {
    setter: Dispatch<any>
}
export type formComponentProps = BasicPredictionFormProps;
export type PredictionOptionForm = (props: formComponentProps) => React.ReactNode;

import { sleep, clampHourValue } from './utils';
import {fetchData} from "./basicPrediction/BasicPredictionFormAPI.ts";
import {transformResponseRegion} from "../UkraineMap/RegionsAPI.ts";

export const LOADING_MESSAGE = "Wait...";
const FALSE_MESSAGE = "There will be no alarm";
const TRUE_MESSAGE = "There will be an alarm"

export const handleInputBlur = (e: React.FormEvent<HTMLInputElement>) => {
    const input = e.currentTarget;
    input.value = clampHourValue(Number.parseInt(input.value, 10)).toString();
};

export const handleSubmit = async (
    setter: Dispatch<any>,
    getSelectValue: () => string | undefined,
    getInputValue: () => string | undefined,
    toggleButton: Dispatch<any>,
) => {
    const region = getSelectValue();
    const hour = getInputValue();

    if (!region || !hour) return;
    setter(LOADING_MESSAGE);
    toggleButton(true);

    try {
        await sleep(600);
        const data = await fetchData(region, hour);

        if (!data?.city_address) return;

        const message = data.prediction ? TRUE_MESSAGE : FALSE_MESSAGE;
        setter(`${message} in ${data.hour_to_add} hour(s) in ${transformResponseRegion(data)}`);

    } catch (error) {
        setter(`Stars didn't align, nothing was predicted`);
        console.warn(error);
    }
    toggleButton(false);
};
