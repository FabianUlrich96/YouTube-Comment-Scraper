import {Col, Row} from "react-bootstrap"

function NotFound() {
    return (
        <>
            <Row className={"pageContainer"}>
                <Col>
                    <h1>404</h1>
                    <h2>Page not found</h2>
                </Col>
            </Row>
        </>
    )
}

export default NotFound