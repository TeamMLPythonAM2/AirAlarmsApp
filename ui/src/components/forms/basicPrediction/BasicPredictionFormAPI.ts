
const BASE_ROUTE = 'http://13.61.68.34:8796';
export type BasicPredictionType = {city: string, hour: string}
export type BasicPredictionResponseType = {
    "prediction": boolean,
    "city_address": string,
    "hour_to_add": number
}

export async function fetchData(
    region: string | undefined,
    range: string | undefined
): Promise<BasicPredictionResponseType | undefined> {
        if (!region || !range) return;
        return await getPrediction(region, range)
}

const getPrediction = async (region: string, range: string) => {
    if (!region) return "";

    const queryData = constructQueryData(region, range);
    const query_url = `${BASE_ROUTE}/prediction`;

    const response = await fetch(query_url, {
        method: "GET",
        headers: {
            ...queryData,
            key: "j8hhZHBR5DmyaEBjMvwi6g9hVwkgSAQRiPLwr5QjGNYarRfac"
        }
    });
    return await response.json();
}

const constructQueryData = (region: string, range: string): BasicPredictionType => {
    return { city: region, hour: `${range}` };
}

