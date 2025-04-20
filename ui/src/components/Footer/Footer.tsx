import './Footer.css'

const TEAM_MEMBERS = [
    "Sukhodolskyi Dmytro",
    "Polishchuk Yurii",
    "Udovychenko Kateryna",
    "Skoromnov Oleksandr",
    "Kyliukh Viktor"
]

const Footer = () => {

    return <footer className="footer">
        <h3>The project is presented by <span className="accent">Team1</span> members: </h3>
        <ul>
            <TeamMembers/>
        </ul>
    </footer>
}

const TeamMembers = () => {
    return TEAM_MEMBERS.map((member, index) => (
        <li key={member + index}>{member}</li>
    ))
}

export default Footer;