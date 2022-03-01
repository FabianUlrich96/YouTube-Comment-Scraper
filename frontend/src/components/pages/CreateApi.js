import {Button, Col, Form, Row} from "react-bootstrap"
import axios from "axios"
import {useState} from "react"
import {A} from "hookrouter"
import {toast, ToastContainer} from "react-toastify"
import 'react-toastify/dist/ReactToastify.css'

function CreateApi() {
    const host = window.location.href
    let host_ip = host.split(':')[1]

    const [form, setForm] = useState({})
    const [errors, setErrors] = useState({})

    const setField = (field, value) => {
        setForm({
            ...form,
            [field]: value
        })

        if (!!errors[field]) setErrors({
            ...errors,
            [field]: null
        })
    }

    const findFormErrors = () => {
        const {name, token} = form
        const newErrors = {}
        // name errors
        if (!name || name === '') newErrors.name = 'cannot be blank!'
        else if (name.length > 30) newErrors.name = 'name is too long!'
        // token errors
        if (!token || token === '') newErrors.token = 'cannot be blank!'

        return newErrors
    }

    function onSubmit(values) {
        values.preventDefault()
        const newErrors = findFormErrors()
        if (Object.keys(newErrors).length > 0) {
            // We got errors!
            setErrors(newErrors)
        } else {
            let data = {
                name: form.name,
                token: form.token,
            }


            axios.post(`http://${host_ip}:1020/apis`, data).then(async res => {
                const successStatus = res.status
                const successMessage = `Status code ${successStatus}: Request successful`
                toast.success(successMessage, {
                    position: "top-center",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                })
            }).catch(err => {
                const errStatus = err.response.status
                const errMessage = `Request failed with status code ${errStatus}`
                toast.error(errMessage, {
                    position: "top-center",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                })
            })
        }
    }

    const session_token = sessionStorage.getItem("access_token")
    if (session_token && session_token !== "" && session_token !== undefined) {
        return (
            <>
                <ToastContainer/>
                <Row className={"pageContainer"}>
                    <Col>
                        <Form onSubmit={onSubmit}>
                            <h2>Add API</h2>
                            <Form.Group className="mb-3" controlId="formName">
                                <Form.Label>API Name</Form.Label>
                                <Form.Control type="text" placeholder="Enter API Name"
                                              onChange={e => setField('name', e.target.value)}
                                              isInvalid={!!errors.name}/>
                            </Form.Group>
                            <Form.Group className="mb-3" controlId="formToken">
                                <Form.Label>API Token</Form.Label>
                                <Form.Control type="text" placeholder="Enter API Token"
                                              onChange={e => setField('token', e.target.value)}
                                              isInvalid={!!errors.token}/>
                            </Form.Group>

                            <Button variant="primary" type="submit">
                                Submit
                            </Button>
                        </Form>
                    </Col>
                </Row>
            </>
        )
    } else {
        return (
            <>
                <Row className={"pageContainer"}>
                    <Col>
                        <p> 401 Unauthorized please login to view the content <A href="/">login</A>.</p>
                    </Col>
                </Row>
            </>
        )
    }
}

export default CreateApi