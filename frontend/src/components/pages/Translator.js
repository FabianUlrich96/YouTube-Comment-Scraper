import {Button, Col, Form, Row} from "react-bootstrap"
import {A} from "hookrouter"
import {toast, ToastContainer} from "react-toastify"
import {useCallback, useEffect, useState} from "react"
import axios from "axios";

function Translator() {
    const host = window.location.href
    let host_ip = host.split(':')[1]
    const [form, setForm] = useState({})
    const [errors, setErrors] = useState({})
    const [jobsDatabase, setJobsDatabase] = useState([])

    const loadJobs = useCallback(() => {
        axios.get(`http://${host_ip}:1020/jobs`).then((response) => {
            console.log(response.data)
            const jobs = []
            const result_data = response.data

            result_data.forEach(job => {
                const displayed_name = `${job.job_id} - ${job.name}`
                jobs.push({
                    rendered: <option key={job.name}>{displayed_name}</option>,
                    job_type: job.job_type
                })
            })
            setJobsDatabase(jobs)
        }).catch(error => {
            console.log(error)
        })


    }, [host_ip])

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
        const {name, job} = form
        const newErrors = {}
        // name errors
        if (!name || name === '') newErrors.name = 'cannot be blank!'
        else if (name.length > 30) newErrors.name = 'name is too long!'
        // jobs errors
        if (!job || job === '') newErrors.job = 'select a job!'

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
                selected_job: form.job,
                job_type: "translation"
            }

            axios.post(`http://${host_ip}:1020/jobs`, data).then(async res => {
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


    useEffect(() => {
        loadJobs()
    }, [loadJobs])

    const token = sessionStorage.getItem("access_token")
    if (token && token !== "" && token !== undefined) {
        return (
            <>
                <ToastContainer/>
                <Row className={"pageContainer"}>
                    <Col>
                        <Form onSubmit={onSubmit}>
                            <h2>Create Translator Job</h2>
                            <Form.Group className="mb-3">
                                <Form.Label>Job Name</Form.Label>
                                <Form.Control type="text" placeholder="Enter job name"
                                              onChange={e => setField('name', e.target.value)}
                                              isInvalid={!!errors.name}/>
                            </Form.Group>
                            <Form.Group className="mb-3" controlId="formApi">
                                <Form.Label>Video Job</Form.Label>
                                <Form.Control as='select' onChange={e => setField('job', e.target.value)}
                                              isInvalid={!!errors.api}
                                >
                                    <option value=''>Select a comment job:</option>
                                    {jobsDatabase.filter(option => option.job_type === "comment").map(option => option.rendered)}
                                </Form.Control>
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

export default Translator