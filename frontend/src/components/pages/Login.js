import {Button, Form} from "react-bootstrap"
import {useState, useContext} from "react"
import axios from "axios"
import {Context} from "../../Store"
import {navigate} from 'hookrouter'


function Login() {
    const [state, setState] = useContext(Context)
    if (state.access_token !== "") {
        sessionStorage.setItem("name", state.username)
        sessionStorage.setItem("access_token", state.access_token)
    }

    const name = sessionStorage.getItem("name")
    const token = sessionStorage.getItem("access_token")

    if (name !== null && token !== null) {
        navigate("/home", true)
    }

    const host = window.location.href
    let host_ip = host.split(':')[1]
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const handleLogin = (values) => {
        values.preventDefault()

        let login_data = {
            username: username,
            password: password
        }
        axios.post(`http://${host_ip}:1020/token`, login_data).then(async res => {
            if (res.status === 200) {
                console.log(res.status)
                sessionStorage.setItem("name", username)
                sessionStorage.setItem("access_token", res.data.access_token)
                setState({
                    name: username,
                    access_token: res.data.access_token
                })
                navigate('/home', true)

            } else {
                console.log(res.status)
            }
        })
    }

    return (
        <div className="color-overlay d-flex justify-content-center align-items-center m-lg-4">
            <Form className="rounded p-4 p-sm-3" onSubmit={handleLogin}>
                <Form.Group className="mb-3">
                    <Form.Label>User</Form.Label>
                    <Form.Control type="text" placeholder="Enter username" value={username}
                                  onChange={(e) => setUsername(e.target.value)}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter password" value={password}
                                  onChange={(e) => setPassword(e.target.value)}/>
                </Form.Group>
                <Button variant="primary" type="submit">Login</Button>
            </Form>
        </div>
    )
}

export default Login