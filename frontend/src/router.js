import React from "react"
import Login from "./components/pages/Login"
import Home from "./components/pages/Home"
import VideoScraper from "./components/pages/VideoScraper"
import CommentScraper from "./components/pages/CommentScraper"
import VideoLoader from "./components/pages/VideoLoader"
import Translator from "./components/pages/Translator"
import CreateApi from "./components/pages/CreateApi"

const routes = {
    "/": () => <Login/>,
    "/home": () => <Home/>,
    "/createvideojob": () => <VideoScraper/>,
    "/createcommentjob": () => <CommentScraper/>,
    "/loadvideos": () => <VideoLoader/>,
    "/translator": () => <Translator/>,
    "/createapi": () => <CreateApi/>
}

export default routes