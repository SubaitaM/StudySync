// UploadDocs Page Logic
document.addEventListener("DOMContentLoaded", function () {
    let continueButton = document.getElementById("continueButton");
    if (continueButton) {
        continueButton.addEventListener("click", async function () {
            let response = await fetch('/process_pdf', {
                method: 'POST',
                body: new FormData(document.getElementById("uploadForm"))
            });

            let data = await response.json();
            console.log(data);

            if (data.success) {
                localStorage.setItem('exam_dates', JSON.stringify(data.dates));
                window.location.href = "Loading.html";
            }
        });
    }
});

// Loading Page Logic
if (window.location.pathname.includes("Loading.html")) {
    document.addEventListener("DOMContentLoaded", function () {
        let dates = JSON.parse(localStorage.getItem('exam_dates')) || [];

        fetch('/save_dates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dates: dates })
        }).then(() => {
            window.location.href = "eventLists.html";
        });
    });
}
document.addEventListener("DOMContentLoaded", function () {
    let dates = JSON.parse(localStorage.getItem('exam_dates')) || [];

    fetch('/save_dates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dates: dates })
    }).then(() => {
        window.location.href = "eventLists.html";
    });
});
