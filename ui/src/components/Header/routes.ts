import Home from "../../pages/Home.tsx";
import PredictionOptions from "../../pages/PredictionOptions.tsx";
import Faq from "../../pages/Faq.tsx";
import React from "react";

export type RouteType = {
    path: string,
    label: string,
    component: React.FunctionComponent<any>,
}

export const ROUTES: RouteType[] = [
    {label: 'home', path: '/', component: Home},
    {label: 'prediction', path: '/prediction', component: PredictionOptions},
    {label: 'faq', path: '/faq', component: Faq}
]