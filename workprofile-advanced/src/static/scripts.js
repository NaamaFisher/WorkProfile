/**
 * @param {HTMLDivElement} div
 * @param {number} id 
 */
function handlePersonClick(div, id) {
    const cssClass = div.className;
    if (cssClass === "person-disabled") { return; }
    fetch(`/delete/${id}`, { method: "DELETE" })
        .then(res => {
            if (res.status === 200) {
                const parent = div.parentElement;
                parent.removeChild(div);
                if (parent.children.length === 0) {
                    const grandparent = parent.parentElement;
                    grandparent.removeChild(parent);
                }
            } else {
                alert("Something went wrong");
            }
        })
        .catch(err => console.log(err));
}

function handleClick() {
    document.getElementById('personModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('personModal').style.display = 'none';
}

/**
 * @param {Event} event 
 */
window.onclick = function (event) {
    let modal = document.getElementById('personModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Handle form submission
document.getElementById('addPersonForm').addEventListener('submit', function (event) {
    event.preventDefault();
    // Collect form data
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const age = document.getElementById('age').value;
    const workplace = document.getElementById('workplace').value;
    const address = document.getElementById('address').value;

    // שים לב: השיטה כאן POST (ולא PUT)
    fetch(`/add`, {
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            firstName,
            lastName,
            age,
            workplace,
            address
        })
    }).then(res => {
        if (res.status === 200) {
            res.json().then(id => {
                // יצירת אלמנטים חדשים להוספה לDOM
                const newPerson = document.createElement('div');
                newPerson.className = "person";
                newPerson.onclick = function () {
                    handlePersonClick(this, id);
                };

                const newPersonName = document.createElement('h3');
                newPersonName.innerHTML = `${firstName} ${lastName}`;

                const newPersonAge = document.createElement('p');
                newPersonAge.innerHTML = `Age: ${age}`;

                const newPersonAddress = document.createElement('p');
                newPersonAddress.innerHTML = `Address: ${workplace}`;

                const newPersonWorkplace = document.createElement('p');
                newPersonWorkplace.innerHTML = `Workplace: ${address}`;

                newPerson.appendChild(newPersonName);
                newPerson.appendChild(newPersonAge);
                newPerson.appendChild(newPersonAddress);
                newPerson.appendChild(newPersonWorkplace);

                const people = document.getElementById('tableContainer');
                let parent = people.children[people.children.length - 1];

                if (parent.childElementCount === 3) {
                    parent = document.createElement('div');
                    parent.className = "container";
                    people.appendChild(parent);
                }

                parent.appendChild(newPerson);
            });
        } else {
            alert("Something went wrong");
        }
    }).catch(err => console.log(err));

    closeModal();
});

