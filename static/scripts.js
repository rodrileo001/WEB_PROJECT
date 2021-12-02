//////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
// Chad McLain
// Group Project 2 - Task Intake
// 
// 
/////////////////////////////////////////////////////////////////////////////////////////////////////////




//Send Title of Movie Clicked to Backend
function getTicketNum(btn) {

    task_num = btn.innerHTML;
    // console.log(title);

    const URL = '/task'
    const xhr = new XMLHttpRequest();
    sender = task_num

    xhr.open('POST', URL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: task_num
    }));
    // alert("Movie added to Viewed List")
}