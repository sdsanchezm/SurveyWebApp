( () => {
    console.log("this is survey.js");
})();

function demo(e) {
    e.preventDefault()
    const formx1 = document.getElementById("form1");

    console.log(formx1);
    alert(formSubmited);
    alert("The form was submitted successfully");
}


function submitResponses_test(event) {
    
    event.preventDefault();
    const formx1 = document.querySelector('#form1');
    console.log("this is submitResponses_test");

    let array1 = [];

    Array.from(formx1).forEach( (item) => {
        array1.push(item.value);
    });
    console.log(array1);
    // debugger;

    let op1 = document.querySelectorAll("#input[name='1']").value;
    console.log(op1);

    };

function submitResponses_test2(event) {
    event.preventDefault();
    console.log("this is test 2 -------");

    let select1 = document.querySelectorAll('.answer');
    const token = window.location.pathname.split('/')[2];
    console.log(token);


    arrayResult = [];

    // validating checkboxes ====================
    Array.from(select1).map((x,y) => {
        let obj = {
            questionId: "",
            answer: "",
            token: token
        };
        let o = x;
        // console.log(o);
        const k1 = o.querySelectorAll('input');
        // console.log(k1);
        k1.forEach( (item) => {
            // console.log(item.value, " - ", item.checked);
            if (item.checked){
                obj.questionId = item.id;
                obj.answer = item.value;
                arrayResult.push(obj);
                return;
            };
        });
        // console.log(JSON.stringify(arrayResult));
    });

    // iterating lists ==============================
    Array.from(select1).map((x) => {
        let obj = {
            questionId: "",
            answer: "",
            token: token
        };
        let o = x;
        // console.log(o);
        const k1 = o.querySelectorAll('select');
        // console.log("this is select: ", k1);
        k1.forEach( (item) => {
            // console.log(item.value);
            if (item.value){
                obj.questionId = item.id;
                obj.answer = item.value;
                arrayResult.push(obj);
                return;
            };
        });
        // console.log(JSON.stringify(arrayResult));
    });

    // iterating text ==============================
    Array.from(select1).map((x) => {
        let obj = {
            questionId: "",
            answer: "",
            token: token
        };
        let o = x;
        console.log(o);
        const k1 = o.querySelectorAll('textarea');
        // console.log("this is select: ", k1);
        k1.forEach( (item) => {
            // console.log(item.value);
            // console.log(item.id);
            if (item.value){
                obj.questionId = item.id;
                obj.answer = item.value;
                arrayResult.push(obj);
                return;
            };
        });
        // console.log(JSON.stringify(arrayResult));
    });

    console.log(JSON.stringify(arrayResult));

    

    let urlx = `http://127.0.0.1:5000/userresponses`;
    // console.log(urlx);
    const response = fetch(urlx, {
        method: 'POST', 
        type:'application/json',
        body: JSON.stringify(arrayResult),
    });

     redirectAtEnd();

};


const redirectAtEnd = () => {
    let form1 = document.querySelector('#form1');
    form1.remove();

    let div1 = document.createElement('div');
    div1.classList.add("alert");
    div1.classList.add("alert-success");
    div1.textContent = "Form Submitted Successfully!";

    let main1 = document.querySelector('main');
    main1.append(div1);


};

