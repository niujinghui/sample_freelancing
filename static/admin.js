console.log("admin.js just invoked!");

import '/static/workbench.js';


/*
const login_form = document.getElementById("authenticate");
login_form.addEventListener("submit", evt => {
    evt.preventDefault();
    const data_for_backend = new FormData(login_form);
    fetch("sign_in", {
            "method": 'POST',
            "body": data_for_backend
        })
        .then(response => {
            if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                    response.status);
                return;
            }
            const feedback = response.text();
            feedback.then(r => {
                console.log("回复的信息是：", r);
                document.querySelector("html").innerHTML = r;
            });
        })
        .catch(console.log);
});
*/