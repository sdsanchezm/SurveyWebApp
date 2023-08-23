// This is index.js
// Author: Sergio Sanchez (sdsanchezm@gmail.com)
// Vanilla Javascript created for the final project NoneSurveySystem, in the CS50x course

// function to show questions
const showQuestions1 = () => {
    const body = document.body
    body.append("Hello") // this allows multiple at the same time

    // Create an element 
    const div1 = document.createElement('div');
    const spanH1 = document.createElement('#hi');
    div1.innerText = "Hallo Welt"; // looks at the css to see and validate the html
    div1.textContent = "Hallo Welt 2"; // just looks at the text itself, even the invisible elements
    body.append(div1);

    // datasets allows to get the properties of a tag
    spanH1.dataset.newName = "hi";
    console.log(spanH1.dataset);

    // removenodes
    node.remove()

    // Set attributes:
    spanH1.setAttribute("title", "blabla");
    spanH1.setAttribute("id", "newId");

    // classes 
    spanH1.classList.add('k1');
    spanH1.classList.remove('k1');
    // add the class, remove it or 
    spanH1.classList.toggle('k1');
    spanH1.classList.toggle('k1', true);
    spanH1.classList.toggle('k1', flase);

    // style properties
    spanH1.style.backgroundColor = 'red';
    

}

const showQuestions2 = () => {
    const listQ = document.querySelector('#listQuestions');
    const tr1 = document.createElement('tr');
    const td1 = document.createElement('td');
    const td2 = document.createElement('td');
    const td3 = document.createElement('td');
    const buttonRemove1 = document.createElement('button');
    buttonRemove1.type = "button";
    buttonRemove1.classList.add('btn-sm');
    buttonRemove1.classList.add('btn-danger');
    // buttonRemove1.onclick = test();
    buttonRemove1.onclick = (e) => {
        tr1.remove();
    };
    td1.textContent = "test1";
    td2.textContent = "test2";
    buttonRemove1.textContent = "Remove";
    td3.append(buttonRemove1);
    tr1.append(td1);
    tr1.append(td2);
    tr1.append(td3);
    listQ.append(tr1);
    
};


function createTableElement(text1, text2, text3)
{
    const listQ = document.querySelector('#listQuestions');
    const tr1 = document.createElement('tr');
    const td1 = document.createElement('td');
    const td2 = document.createElement('td');
    const td3 = document.createElement('td');
    
    td1.textContent = text1 | "NotAvailable";
    td2.textContent = text2 | "NotAvailable";
    td3.textContent = text3 | "NotAvailable";

    tr1.append(td1);
    tr1.append(td2);
    tr1.append(td3);

    return tr1;
}

async function fetchInfo (numx)
{
        // fetch data from the groupsets
        let urlx = `http://127.0.0.1:5000/getsets/${numx}`;
        console.log(urlx);
        const response = await fetch(urlx, {
        method: 'GET'
        })
        .then((response) => {
            return response.json();
          })
        .then((data) => {
            let recordsx = data;
            clearTable();
            recordsx.map( (record) => {
                const listQ = document.querySelector('#listQuestions');
                const tr1 = document.createElement('tr');
                const td1 = document.createElement('td');
                const td2 = document.createElement('td');
                const td3 = document.createElement('td');
                const td4 = document.createElement('td');

                td1.textContent = record.groupsetname;
                td2.textContent = record.question;
                td3.textContent = record.question_type;
                
                // Appending nodes
                tr1.append(td1);
                tr1.append(td2);
                tr1.append(td3);
                tr1.append(td4);

                // Appeding to the parent node
                listQ.append(tr1);
            
            });
        })

    return "";
}

// Clear the table dynamically 
function clearTable(){
    const listQ = document.querySelector('#listQuestions');

    while(listQ.firstChild){
        listQ.removeChild(listQ.firstChild)
    }
}

// when click get View Associations, this function is called and the questions
const showQuestions3 = (num) => {
    fetchInfo(num);
};

// Function to pass data from the table to the modal a bit of jquery
$('#exampleModal').on('show.bs.modal', function (event) {
    let gsx = $(event.relatedTarget).data('gs1');
    $(this).find('#inputgs1').val(gsx);
    console.log(gsx);
});

// Function to 
async function addsets(){
    let qsx = document.getElementById('listQ1').value;
    let gsx = document.getElementById('inputgs1').value;
    let t = {
        gsx:gsx,
        qsx:qsx
    };

    let urlx = `http://127.0.0.1:5000/addsets`;
    console.log(urlx);
    const response = await fetch(urlx, {
    method: 'POST', 
    type:'application/json',
    body: JSON.stringify(t),
    
    })
    .then( res => {
        console.log('res1:', res);
        setTimeout(function() { alert2('Operation Completed', 'primary'); }, 100);

        });
};


const alertPlaceholder = document.getElementById('liveAlertPlaceholder')

const alertX = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}


const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    alert('Nice, you triggered this alert message!', 'success')
  })
}

function alert2(message, type){
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" id="superAlert" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')

    alertPlaceholder.append(wrapper)    
    setTimeout(function() { document.querySelector('#superAlert').remove(); }, 3000);
}

// function to copy the groupset link to clipboard
// function used in groupsets.html
async function copy1(num) {
    try {
        const b1 = document.querySelector('#b-'+num);
        console.log(b1);
        const b3 = b1.dataset.abc1;
        console.log(b3);
        b2 = `http://127.0.0.1:5000/survey/`+b3;
        await navigator.clipboard.writeText(b2);
        console.log('Content copied to clipboard');
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  }

