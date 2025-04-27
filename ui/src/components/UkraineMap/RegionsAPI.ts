import {SPECIAL_REGIONS} from "../../hooks/useAlarmMapSocket.ts";
import {BasicPredictionResponseType} from "../forms/basicPrediction/BasicPredictionFormAPI.ts";

export const REGIONS = [
  "kirovogradska",
  "hersonska",
  "zaporizhska",
  "dnipropetrovska",
  "mykolaivska",
  "odeska",
  "vinitska",
  "cherkaska",
  "kyivska",
  "zhytomyrska",
  "hmelnytska",
  "rivnenska",
  "volynska",
  "lvivska",
  "ternopilska",
  "ivanofrankivska",
  "chernivetska",
  "zakarpatska",
  "poltavska",
  "chernihivska",
  "donetska",
  "kharkivska",
  "luhanska",
  "crimea",
  "sumska",
  "kyiv"
];

export const REGION_TO_CITY_MAP: Record<string, string> = {
  'kirovogradska': 'Kropyvnytskyi',
  'hersonska': 'Kherson',
  'zaporizhska': 'Zaporozhye',
  'dnipropetrovska': 'Dnipro',
  'mykolaivska': 'Mykolaiv',
  'odeska': 'Odesa',
  'vinitska': 'Vinnytsia',
  'cherkaska': 'Cherkasy',
  'kyivska': 'Kyiv oblast',
  'zhytomyrska': 'Zhytomyr',
  'hmelnytska': 'Khmelnytskyi',
  'rivnenska': 'Rivne',
  'volynska': 'Lutsk',
  'lvivska': 'Lviv',
  'ternopilska': 'Ternopil',
  'ivanofrankivska': 'Ivano-Frankivsk',
  'chernivetska': 'Chernivtsi',
  'zakarpatska': 'Uzhgorod',
  'poltavska': 'Poltava',
  'chernihivska': 'Chernihiv',
  'donetska': 'Donetsk',
  'kharkivska': 'Kharkiv',
  'sumska': 'Sumy',
  'kyiv': 'Kyiv'
};

export const CITY_TO_REGION_MAP: Record<string, string> = {
  'Uzhgorod': 'zakarpatska',
  'Mykolaiv': 'mykolaivska',
  'Lviv': 'lvivska',
  'Lutsk': 'volynska',
  'Chernihiv': 'chernihivska',
  'Chernivtsi': 'chernivetska',
  'Vinnytsia': 'vinitska',
  'Kharkiv': 'kharkivska',
  'Ternopil': 'ternopilska',
  'Kyiv': 'kyiv',
  'Kyiv oblast': 'kyivska',
  'Rivne': 'rivnenska',
  'Cherkasy': 'cherkaska',
  'Odesa': 'odeska',
  'Zaporozhye': 'zaporizhska',
  'Zhytomyr': 'zhytomyrska',
  'Kherson': 'hersonska',
  'Khmelnytskyi': 'hmelnytska',
  'Ivano-Frankivsk': 'ivanofrankivska',
  'Dnipro': 'dnipropetrovska',
  'Kropyvnytskyi': 'kirovogradska',
  'Poltava': 'poltavska',
  'Sumy': 'sumska',
  'Donetsk': 'donetska'
};

export const transformResponseRegion = (data: BasicPredictionResponseType) => {
  return REGIONS_TRANSLATED[CITY_TO_REGION_MAP[data.city_address]]
}

export const REGIONS_TRANSLATED: Record<string, string> = {
  kirovogradska: "Kirovohradska Oblast",
  hersonska: "Khersonska Oblast",
  zaporizhska: "Zaporizska Oblast",
  dnipropetrovska: "Dnipropetrovska Oblast",
  mykolaivska: "Mykolaivska Oblast",
  odeska: "Odeska Oblast",
  vinitska: "Vinnytska Oblast",
  cherkaska: "Cherkaska Oblast",
  kyivska: "Kyivska Oblast",
  zhytomyrska: "Zhytomyrska Oblast",
  hmelnytska: "Khmelnytska Oblast",
  rivnenska: "Rivnenska Oblast",
  volynska: "Volynska Oblast",
  lvivska: "Lvivska Oblast",
  ternopilska: "Ternopilska Oblast",
  ivanofrankivska: "Ivano-Frankivska Oblast",
  chernivetska: "Chernivetska Oblast",
  zakarpatska: "Zakarpatska Oblast",
  poltavska: "Poltavska Oblast",
  chernihivska: "Chernihivska Oblast",
  donetska: "Donetska Oblast",
  kharkivska: "Kharkivska Oblast",
  luhanska: "Luhanska Oblast",
  crimea: "Crimea",
  sumska: "Sumska Oblast",
  kyiv: "Kyiv"
};

export type I18Option = {value: any, label: string};

export const regionsToI18Options: I18Option[] = REGIONS
  .filter(region => !SPECIAL_REGIONS.includes(region))
  .map(region =>
      ({
        value: REGION_TO_CITY_MAP[region],
        label: REGIONS_TRANSLATED[region],
      })
  )