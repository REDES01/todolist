import axios from "axios"
import React, {useEffect, useState} from "react";
import AddToDo from "./AddToDo.tsx";
import {formatDateForInput} from "./utils.ts";


export interface todo {
    id:number,
    content:string,
    is_done:boolean,
    end_date:Date,
    subtasks?:subtask[]
}

interface subtask{
    id:number,
    content:string
    is_done:boolean
}



function ToDos(){

    const [todos,setTodos]=useState<todo[]>([])


    useEffect(() => {
        refresh()
    }, []);

    function refresh(){
        axios.get("http://127.0.0.1:8000/todos").then((res)=>{
            const converted= res.data.map((item:todo)=>(
                {
                    ...item,
                    end_date:new Date(item.end_date)
                }))
            setTodos(converted)
            console.log(res.data)
        }).catch((err)=>{
            console.error(err)
        })
    }

    // the function to archiveTodo
    function archiveTodo(id:number) {
        console.log(id)
        axios.delete(`http://127.0.0.1:8000/todos/${id}`)
            .then((res)=>{
                refresh()
                console.log(res.data)
            })
            .catch((err)=>{
                console.error(err)
            })
    }


    function changeIsDone(index:number) {
        const updatedTodos=[...todos]
        updatedTodos[index].is_done=!updatedTodos[index].is_done
        setTodos(updatedTodos)
        saveTodo(index)
    }


    function changeContent(index:number,e:React.FocusEvent<HTMLParagraphElement>) {
        if((e.target as HTMLInputElement).innerText!=todos[index].content){
            const updatedTodos=[...todos]
            updatedTodos[index].content=(e.target as HTMLInputElement).innerText
            setTodos(updatedTodos)
            saveTodo(index)
        }
    }

    function handleTimeChange(index:number,e: React.ChangeEvent<HTMLInputElement>) {
            const updatedTodos=[...todos]
            updatedTodos[index].end_date=new Date(e.target.value)
            setTodos(updatedTodos)
            saveTodo(index)
    }
    function saveTodo(index:number){
        axios.put(`http://127.0.0.1:8000/todos/${todos[index].id}`,{
            content:todos[index].content,
            is_done:todos[index].is_done,
            end_date:todos[index].end_date
        })
            .then((res)=>{
            console.log(res.data)
        }).catch((err)=>{
            console.error(err)
        })
    }


    function createSubtasks(id:number) {
        // setTodos(prev=>
        //     prev.map((t,i)=>
        //         i===id
        //             ?{...t,subtasks:[...(t.subtasks??[]),{content,is_done:false}]}
        //             :t
        //     )
        // )

        // axios.post(`http://127.0.0.1:8000/todos/${id}/subtasks`,{
        //     content:content,
        //     is_done: false,
        // })
        //     .then((res)=>{
        //         refresh()
        //         console.log(res.data)
        // }).catch((err)=>{
        //     console.error(err)
        // })

        axios.post(`http://127.0.0.1:8000/todos/${id}/subtasks/generate`,{
        })
            .then((res)=>{
                refresh()
                console.log(res.data)
        }).catch((err)=>{
            console.error(err)
        })
    }

    function finishSubtask(id:number) {
        axios.delete(`http://127.0.0.1:8000/subtasks/${id}`)
            .then((res)=>{
                refresh()
                console.log(res.data)
            })
            .catch((err)=>{
                console.error(err)
            })

        refresh()
    }

    return (
        <div>
            {todos.map((item,index)=>(
                <div key={index} className="todo-card">

                    <p contentEditable onBlur={(e)=>changeContent(index,e)} className="todo-content" >
                        {item.content}
                    </p>

                    <div className="todo-content">
                        end date:
                        <input type="datetime-local" value={formatDateForInput(item.end_date)} onChange={(e)=>handleTimeChange(index,e)}/>
                        <div style={{ userSelect: 'none' ,display:'inline'}} onClick={()=>changeIsDone(index)}>{item.is_done?"✅":"❌"}</div>
                        <button className="archive-button" onClick={()=>archiveTodo(item.id)}>archive</button>
                        <button onClick={()=>createSubtasks(item.id)}>create subtasks</button>

                    </div>
                    {item.subtasks&&(
                        <ul>
                            {item.subtasks.map((subtask,subIndex)=>(
                                <li key={subIndex} >
                                    {subtask.content}
                                    <button onClick={()=>finishSubtask(subtask.id)}>archive</button>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>

            ))}


            <AddToDo refresh={refresh}></AddToDo>
        </div>
    )
}


export default ToDos
