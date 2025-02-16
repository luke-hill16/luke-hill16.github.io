import http from "./http"
const getAbhsentTypes=()=>{
    const path='/absent/type'    
    return http.get(path)
}
const getResponder=()=>{
    const path="/absent/responder"
    return http.get(path)
}
const applyAbsent=(data)=>{
    const path="/absent/absent"
    return http.post(path,data)}


//const getMyAbsents=(page=1)=>{      const path="/absent/absent?who=my&page="+page
const getMyAbsents=(page)=>{
    const path="/absent/absent?who=my"
    return http.get(path)

}

export default{
    getAbhsentTypes,
    getResponder,
    applyAbsent,
    getMyAbsents,

}