import React from "react";
import { useRef } from "react";
import { Button } from "react-bootstrap";

export default function Login ({setLoggedIn}) {

    const userRef=useRef(null);
    const passwordRef=useRef(null);
    function submitButtonHander(){
        let username=userRef.current.value;
        let password=passwordRef.current.value;
        if(username==='user1' && password==='pass1'){
            console.log('Correct')
            setLoggedIn(true)
        }else{
            setLoggedIn(false)
        }
    }
    return (
        <>
            <br/>   
            <input type="text" placeholder="USERNAME" ref={userRef}/>
            <br/>
            <input type="password" placeholder="PASSWORD" ref={passwordRef}/>
            <br/>
            <Button type="submit" onClick={submitButtonHander}>Login</Button>
        </>
    )
}