import {Button, Container, Form, Nav, Navbar, NavDropdown} from "react-bootstrap"
import {ReactComponent as Logo} from "../../logo.svg"
import {navigate, usePath} from "hookrouter"
import {Context} from "../../Store"
import {useContext} from "react"

function Header() {
    const [state, setState] = useContext(Context)
    if (state.access_token !== "") {
        console.log(state.access_token)
        console.log(state)
        sessionStorage.setItem("name", state.name)
        sessionStorage.setItem("access_token", state.access_token)
    }

    const name = sessionStorage.getItem("name")
    const token = sessionStorage.getItem("access_token")

    let location = usePath()

    function logout() {
        setState({
            name: "",
            access_token: ""
        })
        sessionStorage.clear()
        navigate("/")
    }

    if (token && token !== "" && token !== undefined) {
        return (
            <>
                <Navbar bg="light" expand="lg">
                    <Container fluid>
                        <Navbar.Brand href="/home">
                            <Logo width={"40px"} height={"40px"}/>
                            YouTube - Scraper</Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                        <Navbar.Collapse className="justify-content-end">
                            <Nav activeKey={location.pathname} className="container-fluid">
                                <NavDropdown title="Video" id="basic-nav-dropdown">
                                    <NavDropdown.Item href="/createvideojob">Video Scraper</NavDropdown.Item>
                                    <NavDropdown.Item href="/loadvideos">Load Videos</NavDropdown.Item>
                                </NavDropdown>
                                <Nav.Link href="/createcommentjob">Comment Scraper</Nav.Link>
                                <Nav.Link href="/translator">Translator</Nav.Link>
                                <Nav.Link href="/createapi">Create API</Nav.Link>
                                <Form className="ms-auto">
                                    <Button className={"headerButton"} onClick={logout}>Logout {name}</Button>
                                </Form>
                            </Nav>
                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </>
        )
    } else {

        return (
            <>
                <Navbar bg="light" expand="lg">
                    <Container fluid>
                        <Navbar.Brand href="/login">
                            <Logo width={"40px"} height={"40px"}/>
                            YouTube - Scraper</Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                        <Navbar.Collapse className="justify-content-end">
                            <Nav activeKey={location.pathname} className="container-fluid">
                            </Nav>
                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </>
        )
    }
}

export default Header

