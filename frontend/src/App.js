import './App.css'
import {useRoutes} from 'hookrouter'
import Routes from './router'
import Header from "./components/nav/Header"
import {Container} from "react-bootstrap"
import Store from "./Store"
import NotFound from "./components/pages/NotFound"


function App() {
    const match = useRoutes(Routes)
    return (
        <>
            <Store>
                <Container fluid>
                    <Header/>
                    <div className="container">{match || <NotFound/>}</div>
                </Container>
            </Store>
        </>
    )
}

export default App