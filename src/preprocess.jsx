import React from "react";
import { useRef } from "react";
export default function Preprocess(){
    let fileRef=useRef(null);
    


    return (<>
        
        <input type="file" id="ctrl" directory="" webkitdirectory="" ref={fileRef}/>
        <button onClick={console.log(fileRef)}></button>
    </>)
}