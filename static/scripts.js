// create new todo
document.getElementById('form').onsubmit = (e) => {  //trigger
    e.preventDefault();  //stops the form from refreshing the page.
    // Get the input value
    const description = document.getElementById('description').value;

    // Validate the input
    if (!description.trim()) {
        alert("Please enter a valid description.");
        return;
    }
    fetch('/todos/create',{ //send input data as a Json aobject to the '/todos/creat' endpont on the server
        method: 'POST',
        body: JSON.stringify({ description: description }),
        headers: { 'Content-Type': 'application/json' } //specifies the data being sent in JSON format, must include
    })
    .then((response) => { //the server respons with JSON data
        return response.json();
    }) 
    .then((jsonResponse) => {
        console.log(jsonResponse);
        const liItem = document.createElement('li');
        // liItem.innerHTML = jsonResponce['description'];
        liItem.innerHTML = `
            <input data-id="${jsonResponse.id}" class="completed" type="checkbox">
            ${jsonResponse['description']}
        `;
        document.getElementById('todo').appendChild(liItem);
    })
    .catch ((error)=>{ //error handling
        console.log(error);
        // document.getElementById('error').className='';
        alert("something is wrong!")
    })
}

// update completed for todo
const checkboxes = document.querySelectorAll('.completed');
for (let i = 0 ; i < checkboxes.length ; i++) {
    const checkbox = checkboxes[i];
    checkbox.onchange = ((e) => {
        console.log(e);
        const completed_update = e.target.checked;
        const id = e.target.dataset['id']
        console.log(id, completed_update)
        fetch (`/todos/${id}/update-completed`,{
            method:"POST",
            body: JSON.stringify({'completed': completed_update}),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .catch ((error)=>{ //error handling
        console.log(error);
        // document.getElementById('error').className='';
        alert("something is wrong!")
        })    
    })
}



document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            console.log(event.target);
            const todoId = event.target.getAttribute('data-id');
            console.log(todoId);

            try {
                const response = await fetch (`/todos/${todoId}/delete`,{
                    method:"POST",
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const item = event.target.closest('li');
                    item.remove();
                } else {
                    console.error('Failed to delete');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
});