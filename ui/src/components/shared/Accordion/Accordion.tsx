import React, { useState } from "react";
import './Accordion.css'

export type AccordionProps = {
    accordionHead: React.ReactNode;
    accordionBody: React.ReactNode;
}

const Accordion = ({accordionHead, accordionBody}: AccordionProps) => {
    const [
        isOpen,
        toggleOpen
    ] = useState<boolean>(false);

    function handleToggle(e: React.MouseEvent) {
        e.stopPropagation();
        toggleOpen(prev => !prev);
    }

    return <div className="custom-accordion">
        <div className="custom-accordion-head" onClick={handleToggle}>
            {accordionHead}
            <i className="bi bi-chevron-down"></i>
        </div>
        <div className={"custom-accordion-body " + (isOpen ? "open" : "")}>
            <div className="inner-wrap">
                {accordionBody}
            </div>
        </div>
    </div>
}

export default Accordion;