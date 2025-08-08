import React, {useState} from "react";
import axios from "axios";
import {formatDateForInput} from "./utils.ts";




function AddToDo({refresh}:{refresh:()=>void}){
    //const [username,setUsername]=useState<string>("")
    const [content,setContent]=useState<string>("")
    const [endDate, setEndDate]=useState<string>(formatDateForInput(new Date()))

    function handleSubmit(e:React.FormEvent) {
        e.preventDefault()
        axios.post("http://127.0.0.1:8000/todos",{
            content:content,
            is_done:false,
            end_date:endDate
        })
            .then((res)=>{
                console.log("added",res.data)
                setContent("")
                refresh()
            })
            .catch((e)=>console.error(e))
    }


    return (
        <form onSubmit={handleSubmit} className="add-todo">
            <input
                type="text"
                value={content}
                onChange={(e)=>setContent(e.target.value)}
                placeholder="enter todo"/>
            <p>enter end date</p>
            <input type="datetime-local" value={endDate} onChange={(e)=>setEndDate(e.target.value)}/>

            <button type="submit">Add</button>
        </form>
    )
}

export default AddToDo