
const BASE_ROUTE = 'http://localhost:3000/';
export type BasicPredictionType = {region: string, datetime: string}

export async function fetchData(region: string | undefined){
        if (!region) return;
        return await getPrediction(region)
}

const getPrediction = async (region: string) => {
    if (!region) return "";
    const urlParams = new URLSearchParams(constructQueryData(region));
    const query_url = `${BASE_ROUTE}/prediction/${urlParams.toString()}`;
    const response = await fetch(query_url);
    const responseData = await response.json();
    return JSON.parse(responseData);
}

const constructQueryData = (region: string): BasicPredictionType => {
    return {region: region, datetime: new Date().toISOString()}
}
