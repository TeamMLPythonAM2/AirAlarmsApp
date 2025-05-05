import {BASE_REQUEST_URL} from "../../../consts.ts";

export type PredictionType = {city: string};

export type AlarmsForDayPrediction = {
  last_prediction_time: string;
  regions_forecast: {
    [city: string]: {
      [hour: string]: boolean;
    };
  };
};

export type ForecastData = {
  prediction: AlarmsForDayPrediction;
  city_address: string;
};

export async function fetchData(
    region: string | undefined,
): Promise<ForecastData | undefined> {
    if (!region) return;
    return await getPrediction(region)
}

const getPrediction = async (region: string) => {
    if (!region) return "";

    const queryData = constructQueryData(region);
    const query_url = `${BASE_REQUEST_URL}/api/alarms/all`;
    console.log(query_url)
    const response = await fetch(query_url, {
        method: "GET",
        headers: {
            ...queryData,
            key: "j8hhZHBR5DmyaEBjMvwi6g9hVwkgSAQRiPLwr5QjGNYarRfac"
        }
    });

    if(!response.ok)
        throw new Error("Failed fetching response");

    return await response.json();
}

const constructQueryData = (region: string): PredictionType => {
    return { city: region };
}

