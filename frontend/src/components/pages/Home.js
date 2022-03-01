import axios from "axios"
import BootstrapTable from "react-bootstrap-table-next"
import {Col, ProgressBar, Row, Tab, Tabs} from "react-bootstrap"
import {useCallback, useEffect, useState} from "react"
import {A} from 'hookrouter'

function queryFormatter(cell, row) {
    if (row.query) {
        return (
            <p>{cell}</p>
        )
    }else{
        return (
            <p>-</p>
        )
    }
}
function statusFormatter(cell, row){
    if(row.status && row.total){
    let status = cell
    let total = row.total
    let now = status/total*100
    let label = `${status}/${total}`
    return (
        <ProgressBar now={now} label={label}/>
    )}
    if(row.status &&! row.total){
        return (
            <p>{cell}</p>
        )}
    else{
        return (
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
                <p>-</p>
            </div>
        )
    }

}


const columns = [
    {
        dataField: "name",
        text: "Name",
    },
    {
        dataField: "query",
        text: "Query",
        formatter: queryFormatter
    },
    {
        dataField: "date",
        text: "Date"
    },
    {
        dataField: "done",
        text: "Done"
    },
    {
        dataField: "status",
        text: "Status",
        formatter: statusFormatter
    }
]


function Home() {
    const token = sessionStorage.getItem("access_token")


    const [videoJob, setVideoJob] = useState([])
    const [commentJob, setCommentJob] = useState([])
    const [translationJob, setTranslationJob] = useState([])
    const host = window.location.href
    let host_ip = host.split(':')[1]

    const getJobs = useCallback(() => {
        axios.get(`http://${host_ip}:1020/jobs`)
            .then(response => {
                setCommentJob(response.data.filter(function (item) {
                    return item.job_type === "comment"
                }))
                setVideoJob(response.data.filter(function (item) {
                    return item.job_type === "video"
                }))
                setTranslationJob(response.data.filter(function (item) {
                    return item.job_type === "translation"
                }))
            })
            .catch(error => {
                console.log(error)
            })
    }, [host_ip])

    useEffect(() => {
        const interval = setInterval(() => {
            getJobs()
        }, 250)
        return () => clearInterval(interval)
    }, [getJobs])

    if (token && token !== "" && token !== undefined) {
        return (
            <>
                <Row className={"pageContainer"}>
                    <Col>

                        <Tabs defaultActiveKey="video_scraping_jobs" id="uncontrolled-tab-example" className="mb-3">
                            <Tab eventKey="video_scraping_jobs" title="Video Jobs">
                                <BootstrapTable keyField="id" data={videoJob} columns={columns}/>
                            </Tab>
                            <Tab eventKey="comment_scraping_jobs" title="Comment Jobs">
                                <BootstrapTable keyField="id" data={commentJob} columns={columns}/>
                            </Tab>
                            <Tab eventKey="translator_jobs" title="Translator Jobs">
                                <BootstrapTable keyField="id" data={translationJob} columns={columns}/>
                            </Tab>
                        </Tabs>
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

export default Home

