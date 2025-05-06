import React, {Context, createContext, Dispatch, useContext, useState} from "react";
import './Accordion.css'

export const AccordionsContext: Context<Dispatch<boolean>[]> = createContext([] as Dispatch<boolean>[]);

export type AccordionProps = {
    accordionHead: React.ReactNode;
    accordionBody: React.ReactNode;
}

type WithAccordionContextProps = {
    accordionSetters: Dispatch<boolean>[]
}

function withAccordionsContext<P extends WithAccordionContextProps>(
  Accordion: React.ComponentType<P>
): React.FC<Omit<P, 'accordionSetters'>> {
  return (props) => {
    const accordionContext = useContext(AccordionsContext);

    return (
      <Accordion
        {...(props as P)}
        accordionSetters={accordionContext}
      />
    );
  };
}

const Accordion = (
    {accordionHead, accordionBody, accordionSetters}:
        AccordionProps & WithAccordionContextProps
) => {
    const [
        isOpen,
        toggleOpen
    ] = useState<boolean>(false);

    accordionSetters.push(toggleOpen);

    function handleToggle(e: React.MouseEvent) {
        e.stopPropagation();
        const prev = isOpen;
        accordionSetters.forEach(
            (setter) => setter(false)
        );
        toggleOpen(() => !prev);
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

export default withAccordionsContext(Accordion);