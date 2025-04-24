import {SPECIAL_REGIONS} from "../../hooks/useAlarmMapSocket.ts";

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

export const REGIONS_TRANSLATED: Record<string, string> = {
  kirovogradska: "Kirovohradska Oblast",
  hersonska: "Khersonska Oblast",
  zaporizhska: "Zaporizhska Oblast",
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
  ivanofrankivska: "Ivano-Frankivskska Oblast",
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

export const regionsToI18Options = REGIONS
  .filter(region => !SPECIAL_REGIONS.includes(region))
  .map(region =>
      ({
        value: region,
        label: REGIONS_TRANSLATED[region],
      })
  )