// Asynchronically fetch the data using a POST Request and return an object with the data
async function getData(){
  let gsx = document.querySelector('[name="gs-selector"]').value;
  let surveyurl = document.querySelector('option:checked');
  surveyurl = String(surveyurl.dataset.url);

  let dashboardToken = {
    "token": surveyurl,
  }

  y = [];
  let urlx = `http://127.0.0.1:5000/qra`;
  console.log(urlx);
  const response = await fetch(urlx, {
  method: 'POST',
  headers: {
    'Authorization': 'jaraelgato128'
  },
    type:'application/json',
    body: JSON.stringify(dashboardToken),
  })
  .then(response => response.json())
  .then(response => {console.log('response: ', response); y = response;})
  .catch( (err) => {console.error(err);} );

  return y;
}

// Remove the actual graphs created previously to get a better view of the info without refreshing the page
function clearGraphs(){
  const graphs1 = document.querySelector('#graphs');
  while(graphs1.firstChild){
    graphs1.removeChild(graphs1.firstChild)
  }
}

// get the information to create structures for chartjs
async function sendGroupset(){

  clearGraphs();

  let arrayData = [];
  arrayData = await getData();

  console.log(arrayData);

  arrayData.map( (item) => {

    // array of data -> 
    let labels1 = [];
    // array of labels -> 
    let counts1 = [];
    // id for the canvas node
    let qid = 0;
    // title/question
    let question1 = '';

    item.map( (piece) => {
      labels1.push(piece.response);
      counts1.push(piece.count);
      qid = piece.id;
      question1 = piece.question1;
    });
      let canvasNode = `c-${qid}}`;
      createComponents(canvasNode, question1);
      let ctx = document.getElementById(canvasNode);

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels1,
          datasets: [{
            label: '',
            data: counts1,
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

  });

}

// Testing dashboard
function dashboard_load(){

    let div1 = document.createElement('div');

    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5, 2, 3],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
}

// Creating components in the dashboard.html page (based on the bootstrap 5.2 card structure)
const createComponents = (canvasID, title1) => {

    const main = document.querySelector('#graphs');

    const div1 = document.createElement('div');
    div1.classList.add('col-md-6');
    div1.classList.add('pb-2');
    
    const div2 = document.createElement('div');
    div2.classList.add('card');
    div1.append(div2);
    
    const div3 = document.createElement('div');
    div3.classList.add('card-header');
    div3.classList.add('text-center');
    div2.append(div3);

    const i1 = document.createElement('i');
    i1.classList.add('bi');
    i1.classList.add('bi-question-circle');
    div3.append(i1);

    const span1 = document.createElement('span');
    span1.textContent = title1;
    div3.append(span1);

    const div4 = document.createElement('div');
    div4.classList.add('card-body');
    div2.append(div4);

    const h51 = document.createElement('h5');
    h51.classList.add('card-title');
    h51.textContent = '';
    div4.append(h51);

    const canvas1 = document.createElement('canvas');
    canvas1.setAttribute('id', canvasID);
    div4.append(canvas1);

      main.append(div1);
};
