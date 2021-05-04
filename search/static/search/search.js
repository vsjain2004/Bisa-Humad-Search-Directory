    // Search Directory for the Bisa Humad Jain Samaj
    // Copyright (C) <year>  <name of author>

    // This program is free software: you can redistribute it and/or modify
    // it under the terms of the GNU Affero General Public License as published
    // by the Free Software Foundation, either version 3 of the License, or
    // (at your option) any later version.

    // This program is distributed in the hope that it will be useful,
    // but WITHOUT ANY WARRANTY; without even the implied warranty of
    // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    // GNU Affero General Public License for more details.

    // You should have received a copy of the GNU Affero General Public License
    // along with this program.  If not, see <https://www.gnu.org/licenses/>.

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('sab').addEventListener('click', () => {
        if(document.getElementById('sage').style.display === 'none'){
            document.getElementById('sage').style.display = 'block';
            document.getElementById('ares').style.display = 'block';
            document.getElementById('sname').style.display = 'none';
            document.getElementById('nres').style.display = 'none';
        }
    });

    document.getElementById('snb').addEventListener('click', () => {
        if(document.getElementById('sname').style.display === 'none'){
            document.getElementById('sname').style.display = 'block';
            document.getElementById('nres').style.display = 'block';
            document.getElementById('sage').style.display = 'none';
            document.getElementById('ares').style.display = 'none';
        }
    });

    document.getElementById('sename').addEventListener('click', () => {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const request = new Request(
            `/sname`,
            {headers: {'X-CSRFToken': csrftoken}}
            );
        fetch(request, {
            method: 'POST',
            body : JSON.stringify({
                name: document.getElementById('name').value,
                mname: document.getElementById('mname').value,
                lname: document.getElementById('lname').value,
            }),
            credentials: 'same-origin'
        }).then(response => response.json())
        .then(data => {
            document.getElementById('nres').innerText = '';
            if(data.error){
                document.getElementById('ner').innerText = data.error;
            }
            else{
                document.getElementById('ner').innerText = '';
                const mdiv = document.getElementById('nres');
                data.forEach(person => {
                    let hr = document.createElement('hr');
                    let a = document.createElement('a');
                    a.href = `person/${person.id}`;
                    a.innerText = `${person.SurName}, ${person.Name}`;
                    if(person.MiddleName !== null){
                        a.innerText += ` ${person.MiddleName}`;
                    }
                    mdiv.appendChild(hr);
                    mdiv.appendChild(a);
                })
            }
        })
    })

    document.getElementById('seage').addEventListener('click', () => {
        if(document.getElementById('gender').value === '' || document.getElementById('mstat').value === ''){
            alert('Choose a valid option');
        }
        else{
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const request = new Request(
                `/sadv`,
                {headers: {'X-CSRFToken': csrftoken}}
                );
            fetch(request, {
                method: 'POST',
                body : JSON.stringify({
                    name: document.getElementById('aname').value,
                    mname: document.getElementById('amname').value,
                    lname: document.getElementById('alname').value,
                    gender: document.getElementById('gender').value,
                    miage: document.getElementById('miage').value,
                    maage: document.getElementById('maage').value,
                    mstat: document.getElementById('mstat').value
                }),
                credentials: 'same-origin'
            }).then(response => response.json())
            .then(data => {
                document.getElementById('ares').innerText = '';
                if(data.error){
                    document.getElementById('aer').innerText = data.error;
                }
                else{
                    document.getElementById('aer').innerText = '';
                    const mdiv = document.getElementById('ares');
                    data.forEach(person => {
                        let hr = document.createElement('hr');
                        let a = document.createElement('a');
                        a.href = `person/${person.id}`;
                        a.innerText = `${person.SurName}, ${person.Name}`;
                        if(person.MiddleName !== null){
                            a.innerText += ` ${person.MiddleName}`;
                        }
                        mdiv.appendChild(hr);
                        mdiv.appendChild(a);
                    })
                }
            })
        }
    })
})

function onlyAlphabets(e, t) {
    try {
        if (window.event) {
            var charCode = window.event.keyCode;
        }
        else if (e) {
            var charCode = e.which;
        }
        else { return true; }
        if ((charCode > 64 && charCode < 91) || (charCode > 96 && charCode < 123))
            return true;
        else
            return false;
    }
    catch (err) {
        alert(err.Description);
    }
}